"""
Importing models is used for creating a database model.
"""
from django.db import models


class NotificationPreference(models.Model):
    """
    Represents a user's notification preference for a specific product.
    """

    frequency = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.frequency}"
