from rest_framework import serializers
from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "item_code", "qty", "item_name", "image"]


class AddCartItemSerializer(serializers.Serializer):
    item_code = serializers.CharField(max_length=140)
    qty = serializers.IntegerField(min_value=1, max_value=99, default=1)


class UpdateCartItemSerializer(serializers.Serializer):
    qty = serializers.IntegerField(min_value=1, max_value=99)
