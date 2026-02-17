import hashlib
import hmac
import json
import logging
import threading

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.parsers import JSONParser, BaseParser

from integration.erp_client import ERPNextError, ERPNextUnavailable, ERPNextAuthError, get_erp_client
from .serializers import CheckoutSerializer, OrderSerializer
from .services import checkout_cart_to_order, CheckoutError
from .models import Order
from web.whatsapp import send_sales_invoice_pdf

from rest_framework.throttling import ScopedRateThrottle
from core.throttles import CheckoutRateThrottle

logger = logging.getLogger(__name__)


class PlainTextJSONParser(BaseParser):
    """Parser that handles text/plain as JSON (for ERPNext webhooks)."""
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        return json.loads(stream.read())

class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [CheckoutRateThrottle]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            order = checkout_cart_to_order(user=request.user, checkout_data=serializer.validated_data) # type: ignore
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        except CheckoutError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except (ERPNextAuthError, ERPNextUnavailable, ERPNextError) as e:
            return Response({"error": "ERPNext issue", "details": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({"error": "Unknown error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class MyOrdersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-id")
        data = OrderSerializer(orders, many=True).data
        return Response({"count": len(data), "orders": data})


class MyOrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_id: int):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(OrderSerializer(order).data)


# ---------------------------------------------------------------------------
# ERPNext Webhook: Sales Invoice Submitted
# ---------------------------------------------------------------------------

def _process_sales_invoice_webhook(invoice_name: str) -> None:
    """Background task: fetch Sales Invoice details, find linked Order, send PDF."""
    try:
        client = get_erp_client()

        # Fetch Sales Invoice to get linked Sales Order(s)
        inv_resp = client.request("GET", f"/api/resource/Sales Invoice/{invoice_name}")
        inv_data = inv_resp.get("data") or {}

        # Sales Invoice items have `sales_order` field linking to Sales Order
        sales_orders = set()
        for item in inv_data.get("items") or []:
            so = item.get("sales_order")
            if so:
                sales_orders.add(so)

        if not sales_orders:
            logger.warning("Sales Invoice %s has no linked Sales Orders", invoice_name)
            return

        # Find our Django Order by erp_sales_order_name
        # We store it as "(Online) SAL-ORD-XXXX" so we need to match
        for so_name in sales_orders:
            # Try exact match or with prefix
            order = Order.objects.filter(
                erp_sales_order_name__icontains=so_name
            ).first()
            if order:
                break
        else:
            logger.warning(
                "No Django Order found for Sales Invoice %s (Sales Orders: %s)",
                invoice_name,
                sales_orders,
            )
            return

        # Send the Sales Invoice PDF via WhatsApp
        send_sales_invoice_pdf(phone=order.phone, invoice_name=invoice_name)

    except ERPNextError as exc:
        logger.warning("Failed to process Sales Invoice webhook (%s): %s", invoice_name, exc)
    except Exception as exc:
        logger.exception("Unexpected error processing Sales Invoice webhook: %s", exc)


@method_decorator(csrf_exempt, name="dispatch")
class ERPNextSalesInvoiceWebhook(APIView):
    """Receives webhook from ERPNext when a Sales Invoice is submitted.

    Configure in ERPNext:
      Webhook Doctype: Sales Invoice
      DocType Event: on_submit
      Request URL: https://your-domain.com/api/webhooks/erpnext/sales-invoice/
      Request Method: POST
      Webhook Headers: X-Webhook-Secret = <your secret>
      Webhook Data: { "name": "{{ doc.name }}" }
    """

    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # No auth required, we verify via secret
    parser_classes = [JSONParser, PlainTextJSONParser]  # Accept both JSON and text/plain

    def post(self, request):
        # Verify webhook secret (optional but recommended)
        webhook_secret = getattr(settings, "ERPNEXT_WEBHOOK_SECRET", "")
        if webhook_secret:
            received_sig = request.headers.get("X-Webhook-Secret", "")
            if not hmac.compare_digest(webhook_secret, received_sig):
                logger.warning("ERPNext webhook secret mismatch")
                return Response({"error": "Invalid signature"}, status=status.HTTP_403_FORBIDDEN)

        invoice_name = request.data.get("name")
        if not invoice_name:
            return Response({"error": "Missing 'name' in payload"}, status=status.HTTP_400_BAD_REQUEST)

        logger.info("Received Sales Invoice webhook for: %s", invoice_name)

        # Process in background thread so ERPNext doesn't timeout
        thread = threading.Thread(
            target=_process_sales_invoice_webhook,
            args=(invoice_name,),
            daemon=True,
        )
        thread.start()

        return Response({"status": "accepted", "invoice": invoice_name})

