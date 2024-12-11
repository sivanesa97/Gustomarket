"""
Looking for an admin module
"""
from django.contrib import admin


class PriceTransportAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('amount', 'stock_count', 'minimum_price', 'delivery_charge',
                    'allowing_customer_request')
