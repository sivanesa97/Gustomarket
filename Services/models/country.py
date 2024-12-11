"""
Importing models is used for creating a database model.
"""
from django.db import models


class Country(models.Model):
    """
    A class representing a country such as country name and country code.
    """
    country_name = models.CharField(max_length=90, blank=True, null=True)
    country_code = models.CharField(max_length=5, blank=True, null=True)

    # Return object name as a country name
    def __str__(self):
        return str(self.country_name)
