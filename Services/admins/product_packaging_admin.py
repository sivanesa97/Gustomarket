"""
Looking for an admin module
"""
from django.contrib import admin


class ProductPackagingAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('stacked_layer', 'pieces_per_sku',
                    'waste_per_month', 'product_manufacturer')
