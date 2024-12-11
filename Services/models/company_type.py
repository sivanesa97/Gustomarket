"""
Importing models is used for creating a database model.
"""
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class CompanyType(models.Model):
    """
    A class representing the Type of the Company.
    """
    company_type = models.CharField(
        max_length=255, unique=True, blank=True, null=True)
    ordering = models.IntegerField(unique=True, blank=True, null=True)

    # Return object name as a country type name
    def __str__(self) -> str:
        return str(self.company_type)

    class Meta:
        ordering = ['ordering']


# Signal to update ordering when an instance is deleted
@receiver(post_delete, sender=CompanyType)
def update_ordering_on_delete(sender, instance, **kwargs):
    """
    update_ordering_on_delete
    """
    ordering_value = instance.ordering
    remaining_instances = CompanyType.objects.filter(
        ordering__gt=ordering_value)
    for remaining_instance in remaining_instances:
        remaining_instance.ordering -= 1
        remaining_instance.save()
