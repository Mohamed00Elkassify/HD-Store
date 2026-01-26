from django.urls import path
from .views import CartViewSet

cart_list = CartViewSet.as_view({"get": "list"})
cart_add_item = CartViewSet.as_view({"post": "create"})

cart_item_detail = CartViewSet.as_view({
    "patch": "partial_update",
    "delete": "destroy",
})

urlpatterns = [
    path("cart/", cart_list),
    path("cart/items/", cart_add_item),
    path("cart/items/<int:pk>/", cart_item_detail),
]