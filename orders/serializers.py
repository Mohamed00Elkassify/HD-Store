from rest_framework import serializers
from .models import Order, OrderItem


class CheckoutSerializer(serializers.Serializer):
    payment_method = serializers.ChoiceField(choices=["COD", "VODAFONE_CASH", "CARD"])
    customer_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=50)
    address_line1 = serializers.CharField(max_length=255)
    address_line2 = serializers.CharField(max_length=255, required=False, allow_blank=True, default="")
    city = serializers.CharField(max_length=100)
    notes = serializers.CharField(required=False, allow_blank=True, default="")


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["item_code", "qty", "item_name", "image"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "payment_method",
            "payment_status",
            "customer_name",
            "phone",
            "address_line1",
            "address_line2",
            "city",
            "notes",
            "erp_sales_order_name",
            "created_at",
            "items",
        ]
