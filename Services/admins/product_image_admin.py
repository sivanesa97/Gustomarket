"""
Looking for an admin module
"""
from django.contrib import admin


class ProductPhotoAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('product', 'product_photo')
