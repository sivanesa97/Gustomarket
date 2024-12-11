"""
Importing models is used for creating a database model.
"""
from django.db import models


class LocationType(models.Model):
    """
    A class representing the Type of the Location.
    """
    location_type = models.CharField(
        max_length=255, blank=True, null=True)

    # Return object name as a location type name
    def __str__(self) -> str:
        return str(self.location_type)
