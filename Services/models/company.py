"""
Importing models is used for creating a database model.
"""
from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    """
    A class representing a Company.
    Attributes:
        legal_name (str): The legal name of the Company.
        fancy_name (str): The fancy name of the Company.
        address (str): The address associated with the Company.
        etc.
    """
    logo = models.ImageField(upload_to="logo/", null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    company_type = models.ForeignKey('Services.CompanyType',
                                     on_delete=models.SET_NULL, blank=True, null=True)
    ein = models.CharField(max_length=10, null=True, blank=True, unique=True)
    signature_code = models.CharField(
        max_length=255, null=True, blank=True, unique=True)
    company_phone = models.CharField(
        max_length=15, null=True, blank=True, unique=True)
    company_mobile = models.CharField(
        max_length=12, null=True, blank=True, unique=True)
    address = models.ForeignKey(
        'Services.Address', on_delete=models.SET_NULL, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.company_name)
