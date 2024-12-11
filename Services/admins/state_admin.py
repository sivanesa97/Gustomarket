"""
Looking for an admin module
"""
from django.contrib import admin


class StateAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    # list_display = ('state_name', )
