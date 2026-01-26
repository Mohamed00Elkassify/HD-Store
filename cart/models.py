from django.db import models
from django.contrib.auth.models import User


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart({self.user.username})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    item_code = models.CharField(max_length=140)
    qty = models.PositiveIntegerField(default=1)

    # Optional snapshot fields (helpful for frontend)
    item_name = models.CharField(max_length=255, blank=True)
    image = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("cart", "item_code")

    def __str__(self):
        return f"{self.item_code} x{self.qty}"
