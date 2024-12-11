"""
Looking for an admin module
"""
from django.contrib import admin


class AddressAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('city', )
