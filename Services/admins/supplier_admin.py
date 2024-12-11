"""
Looking for an admin module
"""
from django.contrib import admin


class SupplierAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('first_name', 'stripe_account_id')
