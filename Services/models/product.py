"""
Importing models is used for creating a database model.
"""
from django.db import models


# ********************** Product model start here *******************
class Product(models.Model):
    """
    A class representing a Product.
    Attributes:
    """

    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    supplier = models.ForeignKey('Services.Supplier', on_delete=models.SET_NULL, blank=True, null=True)
    product_title = models.CharField(max_length=255)
    product_category = models.ForeignKey(
        'Services.ProductCategory', on_delete=models.SET_NULL, blank=True, null=True)
    product_sub_category = models.ForeignKey(
        'Services.ProductSubCategory', on_delete=models.SET_NULL, blank=True, null=True)
    product_attribute = models.ManyToManyField('Services.ProductAttribute')
    product_tag = models.ManyToManyField('Services.ProductTag')
    product_packaging = models.ForeignKey(
        'Services.ProductPackaging', on_delete=models.SET_NULL, blank=True, null=True)
    price_transport = models.ForeignKey(
        'Services.PriceTransport', on_delete=models.SET_NULL, blank=True, null=True)
    notification_frequency = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    discussion = models.TextField(blank=True, null=True)
    is_draft = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    review_count = models.PositiveIntegerField(blank=True, null=True, default=0)
    review_sum = models.PositiveIntegerField(blank=True, null=True)
    privacy_level = models.CharField(
        max_length=10, choices=PRIVACY_CHOICES, default='public')
    def __str__(self):
        return str(self.product_title)
# ********************** Product model end here *******************
