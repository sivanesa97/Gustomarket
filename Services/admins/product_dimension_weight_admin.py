"""
Looking for an admin module
"""
from django.contrib import admin


class ProductDimensionAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('dimension_unit', )


class ProductWeightAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('weight_unit', )
