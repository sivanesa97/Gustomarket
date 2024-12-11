"""
Importing models is used for creating a database model.
"""
from django.db import models


class TermsConditions(models.Model):
    """
    A class representing terms and conditions content.
    """
    terms_conditions = models.TextField()

    def __str__(self):
        return "Terms & Conditions"
