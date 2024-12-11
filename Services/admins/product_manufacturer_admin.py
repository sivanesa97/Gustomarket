"""
Looking for an admin module
"""
from django.contrib import admin


class ProductManufacturerAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('manufacture_option',)
