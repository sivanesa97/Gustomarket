"""
Importing models is used for creating a database model.
"""
from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    """
    A class representing a Team.

    Attributes:
        name (str): The name of the Team member.
        email (str): The email address associated with the Team member.
        phone (str): The phone number associated with the Team member.
        etc.
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    supplier = models.ForeignKey('Services.Supplier', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=12, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    seniority = models.ForeignKey(
        'Services.Seniority', on_delete=models.SET_NULL, blank=True, null=True)
    role = models.ManyToManyField('Services.Role')
    profile = models.ManyToManyField('Services.Profile')
    permission = models.ManyToManyField('Services.CustomPermission')
    address = models.ForeignKey(
        'Services.Address', on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    is_agreed_terms = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.first_name} Team Member Of {self.supplier}"
