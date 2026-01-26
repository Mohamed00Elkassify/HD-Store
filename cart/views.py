from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import transaction

from .models import Cart, CartItem
from .serializers import CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from .services import validate_qty_available
from catalog.services import get_product
from integration.erp_client import ERPNextUnavailable, ERPNextAuthError


def erp_error_response(e: Exception):
    if isinstance(e, ERPNextAuthError):
        return Response({"error": "ERPNext auth error", "details": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
    if isinstance(e, ERPNextUnavailable):
        return Response({"error": "ERPNext unavailable", "details": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response({"error": "ERPNext error", "details": str(e)}, status=status.HTTP_502_BAD_GATEWAY)


class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def _get_cart(self, user) -> Cart:
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    def list(self, request):
        """
        GET /api/cart/
        """
        cart = self._get_cart(request.user)
        items = cart.items.all().order_by("-id") # type: ignore
        return Response({"count": items.count(), "items": CartItemSerializer(items, many=True).data})

    @transaction.atomic
    def create(self, request):
        """
        POST /api/cart/items/
        Body: { item_code, qty }
        """
        serializer = AddCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item_code = serializer.validated_data["item_code"] # type: ignore
        qty_to_add = serializer.validated_data["qty"] # type: ignore
        cart = self._get_cart(request.user)

        # lock row if exists to avoid race conditions
        existing = CartItem.objects.select_for_update().filter(cart=cart, item_code=item_code).first()
        current_qty = existing.qty if existing else 0
        target_qty = current_qty + qty_to_add

        ok, available = validate_qty_available(item_code=item_code, requested_qty=target_qty)
        if not ok:
            return Response(
                {"error": "Insufficient stock", "available_qty": available},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if existing:
            existing.qty = target_qty
            # snapshot optional
            try:
                product = get_product(item_code=item_code)
                existing.item_name = product.get("name") or existing.item_name
                existing.image = product.get("image") or existing.image
            except Exception:
                pass

            existing.save(update_fields=["qty", "item_name", "image", "updated_at"])
            return Response(CartItemSerializer(existing).data, status=status.HTTP_200_OK)

        # create new item AFTER validation
        item = CartItem(cart=cart, item_code=item_code, qty=target_qty)
        try:
            product = get_product(item_code=item_code)
            item.item_name = product.get("name") or ""
            item.image = product.get("image") or ""
        except Exception:
            pass

        item.save()
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def partial_update(self, request, pk=None):
        """
        PATCH /api/cart/items/{id}/
        Body: { qty }
        """
        serializer = UpdateCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        qty = serializer.validated_data["qty"] # type: ignore

        cart = self._get_cart(request.user)
        try:
            item = CartItem.objects.get(cart=cart, id=pk)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        ok, available = validate_qty_available(item_code=item.item_code, requested_qty=qty)
        if not ok:
            return Response(
                {"error": "Insufficient stock", "available_qty": available},
                status=status.HTTP_400_BAD_REQUEST,
            )

        item.qty = qty
        item.save(update_fields=["qty", "updated_at"])
        return Response(CartItemSerializer(item).data)

    @transaction.atomic
    def destroy(self, request, pk=None):
        """
        DELETE /api/cart/items/{id}/
        """
        cart = self._get_cart(request.user)
        deleted, _ = CartItem.objects.filter(cart=cart, id=pk).delete()
        if deleted == 0:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
