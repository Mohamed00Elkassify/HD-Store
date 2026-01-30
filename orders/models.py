from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = "CREATED", "Created"
        SYNCED = "SYNCED", "SyncedToERP"
        PROCESSING = "PROCESSING", "Processing"
        SHIPPED = "SHIPPED", "Shipped"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"

    class PaymentMethod(models.TextChoices):
        COD = "COD", "CashOnDelivery"
        VODAFONE_CASH = "VODAFONE_CASH", "VodafoneCash"
        CARD = "CARD", "Card"

    class PaymentStatus(models.TextChoices):
        UNPAID = "UNPAID", "Unpaid"
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)

    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)

    # customer/contact
    customer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)

    # shipping
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    # ERPNext sync fields
    erp_sales_order_name = models.CharField(max_length=140, blank=True)  # e.g. "SAL-ORD-0001"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order({self.id}) - {self.user.username}" # type: ignore


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    item_code = models.CharField(max_length=140)
    qty = models.PositiveIntegerField()

    # snapshot (useful if ERP item name/image changes later)
    item_name = models.CharField(max_length=255, blank=True)
    image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_code} x{self.qty}"

class PaymentTransaction(models.Model):
    class Provider(models.TextChoices):
        COD = "COD", "CashOnDelivery"
        VODAFONE = "VODAFONE", "VodafoneCash"
        CARD = "CARD", "CardGateway"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    provider = models.CharField(max_length=20, choices=Provider.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # type: ignore # optional for now
    reference = models.CharField(max_length=255, blank=True)  # transaction id
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider} {self.status} for Order({self.order_id})" # type: ignore


class VodafoneCashProof(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="vodafone_proof")
    sender_phone = models.CharField(max_length=50)
    reference = models.CharField(max_length=255, blank=True)  # transfer reference if any
    image = models.ImageField(upload_to="vodafone_proofs/")
    created_at = models.DateTimeField(auto_now_add=True)
