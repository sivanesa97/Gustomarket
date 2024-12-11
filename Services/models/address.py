"""
Importing models is used for creating a database model.
"""
from django.db import models


class Address(models.Model):
    """
    A class representing an address such as street, city,
    state, zip code and country.
    """
    supplier = models.ForeignKey(
        'Services.Supplier', on_delete=models.CASCADE, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    address_lane_1 = models.CharField(max_length=255, blank=True, null=True)
    address_lane_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.ForeignKey(
        'Services.State', on_delete=models.CASCADE, blank=True, null=True)
    country = models.ForeignKey(
        'Services.Country', on_delete=models.CASCADE, blank=True, null=True)
    location_type = models.ForeignKey(
        'Services.LocationType', on_delete=models.SET_NULL, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    # Return object name as a city name.
    def __str__(self):
        return f"{self.location}, {self.address_lane_1}, {self.city}, {self.state}, {self.zip_code}"
