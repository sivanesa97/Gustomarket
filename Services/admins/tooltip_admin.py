"""
Looking for an admin module
"""
from django.contrib import admin


class TooltipDataAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('page_name','tooltip_title', 'tooltip_content')


class TooltipAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('page_name',)
