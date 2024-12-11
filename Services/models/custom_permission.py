"""
Importing models is used for creating a database model.
"""
from django.db import models


class CustomPermission(models.Model):
    """
    A class representing a permission.
    """
    permission_name = models.CharField(max_length=255, blank=True, null=True)
    permission_code = models.CharField(max_length=255, blank=True, null=True)

    # Return object name as a permission name
    def __str__(self):
        return str(self.permission_name)
