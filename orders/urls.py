from django.urls import path
from .views import CheckoutView, MyOrdersView, MyOrderDetailView
from .payment_views import (
    UploadVodafoneProofView,
    OrderPaymentsView,
    StaffMarkPaidView,
    StaffUpdateOrderStatusView,
)
from .staff_views import StaffOrdersListView, StaffOrderDetailView

urlpatterns = [
    path("checkout/", CheckoutView.as_view()),
    path("orders/", MyOrdersView.as_view()),
    path("orders/<int:order_id>/", MyOrderDetailView.as_view()),
    
    path("orders/<int:order_id>/vodafone-proof/", UploadVodafoneProofView.as_view()),
    path("orders/<int:order_id>/payments/", OrderPaymentsView.as_view()),

    path("staff/orders/<int:order_id>/mark-paid/", StaffMarkPaidView.as_view()),
    path("staff/orders/<int:order_id>/status/", StaffUpdateOrderStatusView.as_view()),
    
    path("staff/orders/", StaffOrdersListView.as_view()),
    path("staff/orders/<int:order_id>/", StaffOrderDetailView.as_view()),
]
