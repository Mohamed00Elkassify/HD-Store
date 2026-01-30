from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404

from .models import Order, PaymentTransaction, VodafoneCashProof
from .payment_serializers import VodafoneProofUploadSerializer, PaymentTransactionSerializer

from .rules import can_transition

class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class UploadVodafoneProofView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id: int):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        if order.payment_method != Order.PaymentMethod.VODAFONE_CASH:
            return Response({"error": "Order is not Vodafone Cash"}, status=400)
        
        serializer = VodafoneProofUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        proof, created = VodafoneCashProof.objects.update_or_create(
            order=order,
            defaults=serializer.validated_data # type: ignore
        )

        # Create/Update a pending payment transaction
        PaymentTransaction.objects.create(
            order=order,
            provider=PaymentTransaction.Provider.VODAFONE,
            status=PaymentTransaction.Status.PENDING,
            reference=proof.reference,
            notes="Vodafone proof uploaded",
        )
        # Set payment status pending
        order.payment_status = Order.PaymentStatus.PENDING
        order.save(update_fields=["payment_status", "updated_at"])

        return Response({"message": "Proof uploaded", "created": created}, status=201)


class OrderPaymentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_id: int):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        payments = order.payments.all().order_by("-id") # type: ignore
        return Response({"count": payments.count(), "payments": PaymentTransactionSerializer(payments, many=True).data})


class StaffMarkPaidView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStaff]

    def post(self, request, order_id: int):
        order = get_object_or_404(Order, id=order_id)
        order.payment_status = Order.PaymentStatus.PAID
        order.save(update_fields=["payment_status", "updated_at"])
        PaymentTransaction.objects.create(
            order=order,
            provider=PaymentTransaction.Provider.VODAFONE if order.payment_method == Order.PaymentMethod.VODAFONE_CASH else PaymentTransaction.Provider.COD,
            status=PaymentTransaction.Status.SUCCESS,
            notes="Marked as paid by staff",
        )

        return Response({"message": "Order marked as PAID"})


class StaffUpdateOrderStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStaff]

    def post(self, request, order_id: int):
        order = get_object_or_404(Order, id=order_id)
        new_status = request.data.get("status")
        allowed = [s for s, _ in Order.Status.choices]
        if new_status not in allowed:
            return Response({"error": "Invalid status", "allowed": allowed}, status=400)
        if not can_transition(order.status, new_status):
            return Response(
                {"error": "Invalid transition", "from": order.status, "to": new_status},
                status=400
            )
        

        order.status = new_status
        order.save(update_fields=["status", "updated_at"])
        return Response({"message": "Status updated", "status": new_status})
