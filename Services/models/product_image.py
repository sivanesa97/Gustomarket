"""
Importing models is used for creating a database model.
"""
from django.db import models


class ProductPhoto(models.Model):
    """
    A class representing the image of a product.
    """
    product_photo = models.FileField(
        upload_to='product_photo/', null=True, blank=True, default='img/dummy-img.png')
    document_type = models.ForeignKey(
        'Services.DocumentType', on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(
        'Services.Product', on_delete=models.CASCADE)

    def __str__(self):
        return f"Product Image Of {self.product}"
