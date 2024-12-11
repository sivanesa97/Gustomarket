"""
Looking for an admin module
"""
from django.contrib import admin


class SalePresentationAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('presentation_name', )
