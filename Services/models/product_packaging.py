"""
Importing models is used for creating a database model.
"""
from django.db import models


class ProductPackaging(models.Model):
    """
    A class representing packaging of a Product.
    Attributes:
    """
    stacked_layer = models.CharField(max_length=255, blank=True, null=True)
    pieces_per_sku = models.CharField(max_length=255, blank=True, null=True)
    waste_per_month = models.CharField(max_length=255, blank=True, null=True)
    product_manufacturer = models.ForeignKey(
        'Services.ProductManufacturer', on_delete=models.SET_NULL, blank=True, null=True)
    sku_sold = models.ForeignKey(
        'Services.SkuSold', on_delete=models.SET_NULL, blank=True, null=True)
    sku_bulk = models.ForeignKey(
        'Services.SkuBulk', on_delete=models.SET_NULL, blank=True, null=True)
    sku_unit = models.ForeignKey(
        'Services.SkuUnit', on_delete=models.SET_NULL, blank=True, null=True)
    sku_pallet = models.ForeignKey(
        'Services.SkuPallet', on_delete=models.SET_NULL, blank=True, null=True)
    other_sku_sold = models.ForeignKey(
        'Services.OtherSkuSold', on_delete=models.SET_NULL, blank=True, null=True)
    notification_preference = models.ForeignKey(
        'Services.NotificationPreference', on_delete=models.SET_NULL, blank=True, null=True)
    sale_window = models.ForeignKey(
        'Services.SaleWindow', on_delete=models.SET_NULL, blank=True, null=True)
    sale_presentation = models.ForeignKey(
        'Services.SalePresentation', on_delete=models.SET_NULL, blank=True, null=True)
    product_dimension = models.ForeignKey(
        'Services.ProductDimension', on_delete=models.SET_NULL, blank=True, null=True)
    product_weight = models.ForeignKey(
        'Services.ProductWeight', on_delete=models.SET_NULL, blank=True, null=True)
    is_fast = models.BooleanField(default=True)

    def __str__(self):
        return f"Product Packaging - Stacked Layer: {self.stacked_layer}"
# ********************** Product model end here *******************
