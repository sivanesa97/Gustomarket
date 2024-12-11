"""
Importing models is used for creating a database model.
"""
from django.db import models


# ************************Start Payment Term Model*********************
class PaymentTerm(models.Model):
    """
    A class to represent a Payment Term for a Customer.
    """
    term_option = models.CharField(
        max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.term_option}"
# ************* End Payment Term Model**********************
