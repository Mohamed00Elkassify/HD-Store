from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Q

from .models import Order
from .serializers import OrderSerializer
from .payment_views import IsStaff


class StaffOrdersListView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStaff]

    def get(self, request):
        status_q = request.query_params.get("status")
        payment_q = request.query_params.get("payment_status")
        q = request.query_params.get("q", "").strip()

        qs = Order.objects.all().order_by("-id")

        if status_q:
            qs = qs.filter(status=status_q)
        if payment_q:
            qs = qs.filter(payment_status=payment_q)
        if q:
            qs = qs.filter(
                Q(customer_name__icontains=q)
                | Q(phone__icontains=q)
                | Q(erp_sales_order_name__icontains=q)
            )

        data = OrderSerializer(qs[:200], many=True).data
        return Response({"count": len(data), "orders": data})


class StaffOrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStaff]

    def get(self, request, order_id: int):
        order = Order.objects.get(id=order_id)
        return Response(OrderSerializer(order).data)
