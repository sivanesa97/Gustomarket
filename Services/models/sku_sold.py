"""
Importing models is used for creating a database model.
"""
from django.db import models


# ************************Start SkuSold*********************
class SkuSold(models.Model):
    """
    A class represent SKU selling options.
    """
    selling_option = models.CharField(
        max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.selling_option}"
# ************* End SkuSold **********************


# **************** Start Bulk model **********************
class SkuBulk(models.Model):
    """
    A class represent Bulk options of SKU selling options.
    """
    bulk_option = models.CharField(
        max_length=255, blank=True, null=True)
    sku_sold = models.ForeignKey(
        'Services.SkuSold', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.bulk_option}"
# **************** End Bulk model **********************


# **************** Start Unit model **********************
class SkuUnit(models.Model):
    """
    A class represent Unit options of SKU selling options.
    """
    unit_option = models.CharField(
        max_length=255, blank=True, null=True)
    sku_sold = models.ForeignKey(
        'Services.SkuSold', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.unit_option}"
# **************** End Unit model **********************


# ************************ Start Pallet *********************
class SkuPallet(models.Model):
    """
    A class represent Pallet informations.
    """
    sku_sold = models.ForeignKey(
        'Services.SkuSold', on_delete=models.CASCADE)
    pallet_info = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.pallet_info}"
# ************* End Pallet **********************


# ************************ Start OtherSkuSold *********************
class OtherSkuSold(models.Model):
    """
    A class represent other information about sku sold.
    """
    sku_sold = models.ForeignKey(
        'Services.SkuSold', on_delete=models.CASCADE)
    other_info = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.other_info}"
# ************* End OtherSkuSold **********************
