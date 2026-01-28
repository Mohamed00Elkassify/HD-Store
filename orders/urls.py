from django.urls import path
from .views import CheckoutView, MyOrdersView, MyOrderDetailView

urlpatterns = [
    path("checkout/", CheckoutView.as_view()),
    path("orders/", MyOrdersView.as_view()),
    path("orders/<int:order_id>/", MyOrderDetailView.as_view()),
]
