"""
Looking for an admin module
"""
from django.contrib import admin


class CartAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('user', 'product')
