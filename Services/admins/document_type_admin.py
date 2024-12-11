"""
Looking for an admin module
"""
from django.contrib import admin


class DocumentTypeAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('document_type', )
