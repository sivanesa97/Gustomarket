"""
Importing models is used for creating a database model.
"""
from django.db import models


class ProductAttribute(models.Model):
    """
    A class representing the attributes of the products.
    """
    attribute_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.attribute_name)
