from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers

from integration.erp_client import ERPNextAuthError, ERPNextUnavailable
from .services import list_products, get_product, get_stock


def erp_error_response(e: Exception):
    if isinstance(e, ERPNextAuthError):
        return Response({"error": "ERPNext auth error", "details": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
    if isinstance(e, ERPNextUnavailable):
        return Response({"error": "ERPNext unavailable", "details": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response({"error": "ERPNext error", "details": str(e)}, status=status.HTTP_502_BAD_GATEWAY)


class ProductsListParamsSerializer(serializers.Serializer):
    limit = serializers.IntegerField(required=False, min_value=1, max_value=200, default=20)
    offset = serializers.IntegerField(required=False, min_value=0, default=0)
    q = serializers.CharField(required=False, allow_blank=True, max_length=80, default="")


class ProductViewSet(viewsets.ViewSet):
    """
    ViewSet for products coming from ERPNext:
    - list:   GET /api/products/?limit=50
    - retrieve: GET /api/products/{item_code}/
    - stock:  GET /api/products/{item_code}/stock/
    """
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        try:
            params = ProductsListParamsSerializer(data=request.query_params)
            params.is_valid(raise_exception=True)
            limit = params.validated_data["limit"] # type: ignore
            offset = params.validated_data["offset"] # type: ignore
            q = params.validated_data["q"].strip() or None # type: ignore

            products = list_products(limit=limit, offset=offset, q=q)

            return Response(
                {
                    "count": len(products),
                    "limit": limit,
                    "offset": offset,
                    "q": q or "",
                    "products": products,
                }
            )
        except Exception as e:
            return erp_error_response(e)

    def retrieve(self, request, pk=None):
        # pk here will be item_code from the URL
        try:
            product = get_product(item_code=pk) # type: ignore
            return Response(product)
        except Exception as e:
            return erp_error_response(e)

    @action(detail=True, methods=["get"], url_path="stock")
    def stock(self, request, pk=None):
        try:
            payload = get_stock(item_code=pk) # type: ignore
            return Response(payload)
        except Exception as e:
            return erp_error_response(e)
