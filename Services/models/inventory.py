from django.db import models
from django.utils import timezone
from .product import Product

class InventoryChangeType(models.Model):
    name = models.CharField(max_length=50)
    change_status = models.IntegerField(choices=[(-1, 'Reduce'), (0, 'No Change'), (1, 'Add')])
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'inventory_change_types'

class InventoryItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    code = models.CharField(max_length=50, blank=True, null=True)
    count = models.IntegerField(default=0)
    new_count = models.IntegerField(default=0)
    type_of_change = models.ForeignKey(InventoryChangeType, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'inventory_items'
        unique_together = ('product', 'type_of_change')

class InventoryHistory(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    previous_count = models.IntegerField()
    new_count = models.IntegerField()
    type_of_change = models.ForeignKey(InventoryChangeType, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='inventory_history/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventory_history' 