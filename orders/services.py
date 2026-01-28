from datetime import date, timedelta
from typing import Tuple
from django.conf import settings
from django.db import transaction
from cart.models import CartItem, Cart
from cart.services import validate_qty_available
from catalog.services import get_product
from .models import Order, OrderItem
from .erp_services import create_erp_sales_order


class CheckoutError(Exception):
    pass


@transaction.atomic
def checkout_cart_to_order(*, user, checkout_data: dict) -> Order:
    # 1) get cart
    cart, _ = Cart.objects.get_or_create(user=user)
    cart_items = list(cart.items.all()) # type: ignore

    if not cart_items:
        raise CheckoutError("Cart is empty")

    # 2) validate stock for each item (actual_qty only, per your company decision)
    for ci in cart_items:
        ok, available = validate_qty_available(item_code=ci.item_code, requested_qty=ci.qty)
        if not ok:
            raise CheckoutError(f"Insufficient stock for {ci.item_code}. Available: {available}")

    # 3) create Order
    order = Order.objects.create(
        user=user,
        payment_method=checkout_data["payment_method"],
        payment_status=Order.PaymentStatus.UNPAID,
        customer_name=checkout_data["customer_name"],
        phone=checkout_data["phone"],
        address_line1=checkout_data["address_line1"],
        address_line2=checkout_data.get("address_line2", ""),
        city=checkout_data["city"],
        notes=checkout_data.get("notes", ""),
        status=Order.Status.CREATED,
    )

    # 4) create OrderItems (snapshots)
    order_items_payload = []
    for ci in cart_items:
        item_name = ci.item_name
        image = ci.image
        # fallback snapshot from ERPNext if cart has no snapshot
        if not item_name or not image:
            try:
                p = get_product(item_code=ci.item_code)
                item_name = item_name or (p.get("name") or "")
                image = image or (p.get("image") or "")
            except Exception:
                pass

        OrderItem.objects.create(
            order=order,
            item_code=ci.item_code,
            qty=ci.qty,
            item_name=item_name or "",
            image=image or "",
        )
        order_items_payload.append({"item_code": ci.item_code, "qty": ci.qty})

    # 5) create Sales Order in ERPNext automatically
    # delivery date: today + 2 days (placeholder). later can be configurable.
    delivery = (date.today() + timedelta(days=2)).isoformat()

    erp_customer = getattr(settings, "ERPNEXT_DEFAULT_CUSTOMER", "Online Customer")
    erp_resp = create_erp_sales_order(
        customer=erp_customer,
        delivery_date=delivery,
        items=order_items_payload,
        order_notes=order.notes,
    )

    # ERP response shape: often { "data": { "name": "...", ... } }
    so_name = None
    if isinstance(erp_resp, dict):
        so_name = (erp_resp.get("data") or {}).get("name")

    if so_name:
        order.erp_sales_order_name = so_name
        order.status = Order.Status.SYNCED
        order.save(update_fields=["erp_sales_order_name", "status", "updated_at"])

    # 6) clear cart (after successful order + ERP sync)
    cart.items.all().delete() # type: ignore
    return order
