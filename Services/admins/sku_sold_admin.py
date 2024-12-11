"""
Looking for an admin module
"""
from django.contrib import admin


class SkuSoldAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('selling_option',)


class SkuBulkAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('bulk_option',)


class SkuUnitAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('unit_option',)


class SkuPalletAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('pallet_info',)


class OtherSkuSoldAdmin(admin.ModelAdmin):
    """
    Display all fields on the admin site.
    """
    list_display = ('other_info',)
