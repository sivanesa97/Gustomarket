"""
Importing models is used for creating a database model.
"""
from django.db import models
from django.contrib.auth.models import User


class Cart(models.Model):
    """
    A class representing a Product adding in the cart.
    Attributes:
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product} in {self.user}'s cart"
