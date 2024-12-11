from django.db import models
from django.contrib.auth.models import User

class ChangeLog(models.Model):
    model_name = models.CharField(max_length=255)
    instance_id = models.CharField()  # ID of the modified instance
    field_name = models.CharField(max_length=255)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    change_type = models.CharField(max_length=10)  # e.g., 'update', 'create', 'delete'
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.model_name} - {self.field_name} changed"
