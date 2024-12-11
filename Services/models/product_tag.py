"""
Importing models is used for creating a database model.
"""
from django.db import models

# ********************** Tag model start here *******************


class ProductTag(models.Model):
    """
    A class representing the tag of a Product.
    Attributes:
    """
    tag_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.tag_name}"
# ********************** Tag model end here *******************
