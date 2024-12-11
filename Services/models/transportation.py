"""
Importing models is used for creating a database model.
"""
from django.db import models


class Transportation(models.Model):
    """
    Model representing transportation of a product.
    """
    CONDITION_CHOICES = [
        ('stay_outside_weather', 'Can stay in outside weather'),
        ('Dry_Normal', 'Dry / Normal'),
        ('Temperature_controlled', 'Temperature controlled'),
        ('cold', 'Cold'),
        ('frozen', 'Frozen'),
        ('condition', 'Other'),
    ]

    condition = models.CharField(
        max_length=255, choices=CONDITION_CHOICES, blank=True, null=True)

    # Additional field for custom input
    custom_condition = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.condition}"


class HandlingTransport(models.Model):
    """
    Model representing to handle transportation of a product.
    """
    HANDLING_CHOICES = [
        ('internal_transport', 'Internal transport'),
        ('third_part_logistics', 'A third party handles my logistics'),
    ]

    handling_option = models.CharField(
        max_length=255, choices=HANDLING_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.handling_option}"


class ProductCertification(models.Model):
    """
    Model representing certification of a product.
    """
    CERTIFICATION_CHOICES = [
        ('quality_anagement', 'Quality Management System'),
        ('information_security', 'Information Security Management'),
    ]

    certification = models.CharField(
        max_length=255, choices=CERTIFICATION_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.certification}"
