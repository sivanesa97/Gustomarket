"""
Importing models is used for creating a database model.
"""
from django.db import models


class ProductCertificate(models.Model):
    """
    A class representing legal certificate of a product.
    """
    product_certificate = models.FileField(
        upload_to='product_certificate/', null=True, blank=True)
    document_type = models.ForeignKey(
        'Services.DocumentType', on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(
        'Services.Product', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Product Certificate Of {self.product}"
