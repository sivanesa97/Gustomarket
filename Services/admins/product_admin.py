"""
Looking for an admin module
"""
from django.contrib import admin


class ProductAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('product_title', 'product_category', 'product_packaging',
                    'price_transport', 'is_draft', 'is_active', 'supplier')
