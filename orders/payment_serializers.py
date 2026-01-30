from rest_framework import serializers
from .models import VodafoneCashProof, PaymentTransaction


class VodafoneProofUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = VodafoneCashProof
        fields = ["sender_phone", "reference", "image"]


class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = ["id", "provider", "status", "amount", "reference", "notes", "created_at"]
