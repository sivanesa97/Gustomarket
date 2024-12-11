from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models.changelog_models import ChangeLog
from .middleware import get_current_user  # Middleware from the previous example

IGNORED_MODELS = ['Session', 'Migrations']


@receiver(pre_save)
def log_pre_save_changes(sender, instance, **kwargs):
    # Get current user from middleware
    current_user = get_current_user()
    
    # Skip logging if user is anonymous or if model is in ignored list
    if not current_user or current_user.is_anonymous or \
       sender.__name__ in IGNORED_MODELS or \
       sender == ChangeLog or not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    for field in instance._meta.fields:
        field_name = field.name
        old_value = getattr(old_instance, field_name)
        new_value = getattr(instance, field_name)
        if old_value != new_value:
            ChangeLog.objects.create(
                model_name=sender.__name__,
                instance_id=instance.pk,
                field_name=field_name,
                old_value=old_value,
                new_value=new_value,
                change_type="update",
                user=current_user
            )


@receiver(post_save)
def log_post_save(sender, instance, created, **kwargs):
    # Avoid logging ChangeLog itself
    if sender.__name__ in IGNORED_MODELS or sender == ChangeLog or not instance.pk:
        return

    if created:
        # Log creation of a new instance
        ChangeLog.objects.create(
            model_name=sender.__name__,
            instance_id=instance.pk,
            field_name="All Fields",
            old_value=None,
            new_value=str(instance),
            change_type="create",
            user=get_current_user()
        )


@receiver(post_delete)
def log_deletion(sender, instance, **kwargs):
    # Avoid logging ChangeLog itself
    if sender.__name__ in IGNORED_MODELS or sender == ChangeLog or not instance.pk:
        return

    # Log deletion of an instance
    ChangeLog.objects.create(
        model_name=sender.__name__,
        instance_id=instance.pk,
        field_name="All Fields",
        old_value=str(instance),
        new_value=None,
        change_type="delete",
        user=get_current_user()
    )
