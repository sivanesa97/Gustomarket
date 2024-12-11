"""
Importing models is used for creating a database model.
"""
from django.db import models


class Role(models.Model):
    """
    A class representing the role of a team member.
    """
    name = models.CharField(max_length=255, blank=True, null=True)
    custom_permission = models.ManyToManyField('Services.CustomPermission')

    # Return object name as a role name
    def __str__(self):
        return str(self.name)
