"""
Looking for an admin module
"""
from django.contrib import admin


class ProductAttributeAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('attribute_name', )
