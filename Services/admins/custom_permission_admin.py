"""
Looking for an admin module
"""
from django.contrib import admin


class CustomPermissionAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('permission_name', 'permission_code')
