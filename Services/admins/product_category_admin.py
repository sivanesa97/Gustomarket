"""
Looking for an admin module
"""
from django.contrib import admin


class ProductCategoryAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('category_name', )
