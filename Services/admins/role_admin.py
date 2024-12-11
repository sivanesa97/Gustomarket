"""
Looking for an admin module
"""
from django.contrib import admin


class RoleAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('name',)
