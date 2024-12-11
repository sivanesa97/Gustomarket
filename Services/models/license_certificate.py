"""
Importing models is used for creating a database model.
"""
from django.db import models


class LicenseCertificate(models.Model):
    """
    A class representing legal documents of a company.
    """
    license_certificate = models.FileField(
        upload_to='license_certificate/', null=True, blank=True)
    document_type = models.ForeignKey(
        'Services.DocumentType', on_delete=models.SET_NULL, blank=True, null=True)
    supplier = models.ForeignKey(
        'Services.Supplier', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"License Certificate Of {self.supplier}"
