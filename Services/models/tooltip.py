"""
Importing models is used for creating a database model.
"""
from django.db import models


class Tooltip(models.Model):
    """
    Model representing tooltips for various pages.
    """
    page_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.page_name}"


class TooltipData(models.Model):
    """
    Model representing tooltip's data for various pages.
    """
    page_name = models.ForeignKey('Services.Tooltip', on_delete=models.CASCADE)
    tooltip_title = models.CharField(max_length=255, blank=True, null=True)
    tooltip_content = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        Returns a string representation of the tooltip.
        """
        return f"{self.page_name} - {self.tooltip_title}"
