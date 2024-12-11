"""
Importing models is used for creating a database model.
"""
from django.db import models


class ProductPricingHistory(models.Model):
    """
    A class representing a Product's Pricing History.
    """
    product = models.ForeignKey(
        'Services.Product', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pricing History: {self.product.product_title}"
