"""
Looking for an admin module
"""
from django.contrib import admin


class ProductSubCategoryAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('sub_category_name', 'product_category',)
