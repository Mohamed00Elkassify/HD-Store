import pytest
from cart.models import Cart, CartItem
from orders.models import Order

@pytest.mark.django_db
def test_checkout_empty_cart(auth_client):
    res = auth_client.post("/api/checkout/", {
        "payment_method": "COD",
        "customer_name": "Mohamed",
        "phone": "01000000000",
        "address_line1": "Street 1",
        "address_line2": "",
        "city": "Cairo",
        "notes": ""
    }, format="json")
    assert res.status_code == 400

@pytest.mark.django_db
def test_checkout_success_creates_order_and_calls_erp(auth_client, user, mocker):
    # create cart + item
    cart, _ = Cart.objects.get_or_create(user=user)
    CartItem.objects.filter(cart=cart).delete()
    CartItem.objects.create(cart=cart, item_code="SKU007", qty=1)

    # mock ERP call - patch where it's used (in orders.services)
    mock_create_so = mocker.patch("orders.services.create_erp_sales_order")
    mock_create_so.return_value = {"data": {"name": "SAL-ORD-TEST-0001"}}

    payload = {
        "payment_method": "COD",
        "customer_name": "Mohamed",
        "phone": "01000000000",
        "address_line1": "Street 1",
        "address_line2": "",
        "city": "Cairo",
        "notes": ""
    }

    res = auth_client.post("/api/checkout/", payload, format="json")
    assert res.status_code == 201

    # order created
    assert Order.objects.count() == 1
    order = Order.objects.first()
    assert order is not None
    assert order.erp_sales_order_name != ""  # should be set from mocked ERP response

    # ERP called once
    assert mock_create_so.call_count == 1
