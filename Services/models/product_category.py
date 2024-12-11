"""
Importing models is used for creating a database model.
"""
from django.db import models


class ProductCategory(models.Model):
    """
    A class representing the category of the products.
    """
    category_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.category_name)
 