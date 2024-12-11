"""
Looking for an admin module
"""
from django.contrib import admin


class CustomerAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('stripe_customer_id', 'name', 'email')
