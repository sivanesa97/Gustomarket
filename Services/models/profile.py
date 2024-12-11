"""
Importing models is used for creating a database model.
"""
from django.db import models


class Profile(models.Model):
    """
    A class representing the profile of a Team member.
    """
    name = models.CharField(max_length=255, blank=True, null=True)
    custom_permission = models.ManyToManyField('Services.CustomPermission')

    # Return object name as a profile name
    def __str__(self):
        return str(self.name)
