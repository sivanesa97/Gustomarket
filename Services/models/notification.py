"""
Importing models is used for creating a database model.
"""
from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    """
    A class representing a Notification sent to a user.
    Attributes:
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} sent '{self.message}' at {self.timestamp}."
