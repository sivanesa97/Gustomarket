"""
Importing models is used for creating a database model.
"""
from django.db import models


class Payment(models.Model):
    """
    A class representing a payment of an order.
    Attributes:
    """
    paymentID = models.CharField(max_length=255, blank=True, null=True)
    customerID = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, blank=True, null=True)
    status = models.CharField(max_length=20, default='pending')
    payment_method_type = models.CharField(
        max_length=20, blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_type = models.CharField(max_length=10, blank=True, null=True)
    account_holder_type = models.CharField(
        max_length=10, blank=True, null=True)
    account_number_last_4 = models.CharField(
        max_length=4, blank=True, null=True)
    routing_number = models.CharField(max_length=9, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.paymentID} - {self.amount} {self.currency}"
