"""
Looking for an admin module
"""
from django.contrib import admin


class SeniorityAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('seniority',)
