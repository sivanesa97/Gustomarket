"""
Importing models is used for creating a database model.
"""
from django.db import models


class PriceTransport(models.Model):
    """
    A class representing a price and transport of a Product.
    Attributes:
    """
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    minimum_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    delivery_charge = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    stock_count = models.IntegerField(default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.PositiveIntegerField(default=0)
    transportation = models.ForeignKey(
        'Services.Transportation', on_delete=models.SET_NULL, blank=True, null=True)
    handling_transport = models.ForeignKey(
        'Services.HandlingTransport', on_delete=models.SET_NULL, blank=True, null=True)
    certification = models.ForeignKey(
        'Services.ProductCertification', on_delete=models.SET_NULL, blank=True, null=True)
    address = models.ForeignKey(
        'Services.Address', on_delete=models.SET_NULL, blank=True, null=True)
    from_seasonality = models.DateField(blank=True, null=True)
    to_seasonality = models.DateField(blank=True, null=True)
    is_best_transportation = models.BooleanField(default=True)
    is_special_packaging = models.BooleanField(default=True)
    allowing_customer_request = models.BooleanField(default=True)

    def __str__(self):
        return f"Amount: {self.amount}"
