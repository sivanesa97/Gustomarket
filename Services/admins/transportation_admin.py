"""
Looking for an admin module
"""
from django.contrib import admin


class TransportationAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('condition',)


class HandlingTransportAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('handling_option',)


class ProductCertificationAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('certification',)
