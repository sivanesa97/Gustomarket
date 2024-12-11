"""
Importing models is used for creating a database model.
"""
from django.db import models


class ProductManufacturer(models.Model):
    """
    A class representing the manufacturer of the products.
    """
    manufacture_option = models.CharField(
        max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.manufacture_option)
