"""
Importing models is used for creating a database model.
"""
from django.db import models


# ************** Start Product Dimention ***********
class ProductDimension(models.Model):
    """
    Represents product Dimension.
    """

    DIMENSION_CHOICES = [
        ('inch', 'Inches'),
        ('cm', 'Centimeters'),
        ('feet', 'Feet'),
        ('meter', 'Meters'),
        ('other', 'Other'),
    ]

    dimension_unit = models.CharField(
        max_length=20, choices=DIMENSION_CHOICES, default='inch')
    height = models.CharField(max_length=255, blank=True, null=True)
    length = models.CharField(max_length=255, blank=True, null=True)
    width = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.height} x {self.width} x {self.length} {self.dimension_unit}"
# ************** End Product Dimention ***********


# ************** Start Product Weight ***********
class ProductWeight(models.Model):
    """
    Represents product Weight.
    """

    WEIGHT_CHOICES = [
        ('kg', 'Kilograms'),
        ('g', 'Grams'),
        ('oz', 'Ounces'),
        ('other', 'Other'),
    ]

    weight_unit = models.CharField(
        max_length=20, choices=WEIGHT_CHOICES, default='kg')
    weight_value = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.weight_value} {self.weight_unit}"
# ************** End Product Weight ***********
