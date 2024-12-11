"""
Importing models is used for creating a database model,
and User, Group, Company is imported to make a relation to another model.
"""
from django.db import models
from django.contrib.auth.models import User


class Supplier(models.Model):
    """
    A class representing a user profile.

    Attributes:
        email (str): The email address associated with the user.
        full_name (str): The full name of the user.
        birthdate (str): The birthdate of the user in the format 'YYYY-MM-DD'.
        profile_picture (str): URL or file path to the user's profile picture.
        etc.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to="photo/", null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(
        max_length=255, null=True, blank=True, unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    stripe_account_id = models.CharField(max_length=100, blank=True, null=True)
    public = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    company = models.ForeignKey(
        'Services.Company', on_delete=models.SET_NULL, null=True, blank=True)
    terms_conditions = models.ForeignKey(
        'Services.TermsConditions', on_delete=models.SET_NULL, blank=True, null=True)
    is_agreed_terms = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    # Retuen object name as a first name
    def __str__(self):
        return f"Supplier Profile for {self.user}"
