"""
Importing models is used for creating a database model.
"""
from django.db import models


class SalePresentation(models.Model):
    """
    Represents different presentation of sale during the day.
    """

    presentation_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.presentation_name}"
