from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from integration.erp_client import ERPNextError, ERPNextUnavailable, ERPNextAuthError
from .serializers import CheckoutSerializer, OrderSerializer
from .services import checkout_cart_to_order, CheckoutError
from .models import Order

from rest_framework.throttling import ScopedRateThrottle
from core.throttles import CheckoutRateThrottle

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

