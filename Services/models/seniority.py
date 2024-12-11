"""
Importing models is used for creating a database model.
"""
from django.db import models


class Seniority(models.Model):
    """
    A class represent the seniority of a team member.
    """
    seniority = models.CharField(
        max_length=255, unique=True, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.seniority)
