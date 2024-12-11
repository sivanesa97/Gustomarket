from django.db import models
from django.utils import timezone

class InventoryChangeType(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # Link to your Product model
    count = models.IntegerField(default=0)
    new_count = models.IntegerField(default=0)
    type_of_change = models.ForeignKey(InventoryChangeType, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='inventory/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class InventoryHistory(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    previous_count = models.IntegerField()
    new_count = models.IntegerField()
    type_of_change = models.ForeignKey(InventoryChangeType, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='inventory_history/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now) 