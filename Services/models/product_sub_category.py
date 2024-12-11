"""
Importing models is used for creating a database model.
"""
from django.db import models


class ProductSubCategory(models.Model):
    """
    A class representing the category of the products.
    """
    sub_category_name = models.CharField(max_length=255, blank=True, null=True)
    product_category = models.ForeignKey(
        'Services.ProductCategory', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.sub_category_name)
