"""
Looking for an admin module
"""
from django.contrib import admin


class OrderItemAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('order', 'product', 'order_status')
