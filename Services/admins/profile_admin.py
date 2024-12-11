"""
Looking for an admin module
"""
from django.contrib import admin


class ProfileAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('name', )
