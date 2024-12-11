"""
Looking for an admin module
"""
from django.contrib import admin
from Services.models import CompanyType


class CompanyTypeAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('company_type', 'ordering')

    def save_model(self, request, obj, form, change):
        # Check if the ordering field is not set
        if not obj.ordering:
            # Set the ordering field to the next available value
            max_ordering = CompanyType.objects.count()
            obj.ordering = max_ordering + 1

        super().save_model(request, obj, form, change)
