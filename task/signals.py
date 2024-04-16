from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone  # Use Django's timezone for datetime operations
from .models import Task


@receiver(pre_save, sender=Task)
def update_notification_datetime(sender, instance, **kwargs):
    """
    This signal uses for change the notification_datetime field of a task
    if task notification_status changed to notified

    """
    if instance.pk is not None:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return

        if (
            old_instance.notification_status != instance.notification_status
            and instance.notification_status == Task.NOTIFIED
        ):
            instance.notification_datetime = timezone.now()

    if (
        instance.notification_status == Task.NOTIFIED
        and instance.notification_datetime is None
    ):
        instance.notification_datetime = timezone.now()
