"""
Importing models is used for creating a database model.
"""
from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    """
    A class representing a customer.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.ForeignKey(
        'Services.Address', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.email})"
