"""
Importing models is used for creating a database model.
"""
from django.db import models


class State(models.Model):
    """
    A class representing a state such as state name and state code.
    """
    state_name = models.CharField(max_length=255)
    state_zip_code = models.CharField(max_length=20)
    country = models.ForeignKey(
        'Services.Country', on_delete=models.SET_NULL, blank=True, null=True)

    # Return object name as a state name
    def __str__(self):
        return f"{self.state_name}({self.country})"
