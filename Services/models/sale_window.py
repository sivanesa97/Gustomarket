"""
Importing models is used for creating a database model.
"""
from django.db import models


class SaleWindow(models.Model):
    """
    Represents different windows of sale during the day.
    """

    window_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.window_name}"
