from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from task.celery_tasks import send_task_email
from .models import Task


@receiver(pre_save, sender=Task)
def add_task_to_celery(sender, instance, **kwargs):
    """
    Whenever a task is created or its due date is updated, this signal is called to add the task to Celery.
    """
    if instance.pk is None:
        due_datetime = instance.due_datetime
        now = timezone.now()
        time_difference = due_datetime - now
        instance.notification_status = Task.NOTIFIED
        instance.notification_datetime = timezone.now()
        send_task_email.apply_async(
            args=[instance.id], countdown=time_difference.total_seconds()
        )
    else:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return

        if old_instance.due_datetime != instance.due_datetime:
            now = timezone.now()
            time_difference = instance.due_datetime - now
            instance.notification_status = Task.NOTIFIED
            instance.notification_datetime = timezone.now()
            send_task_email.apply_async(
                args=[instance.id], countdown=time_difference.total_seconds()
            )


@receiver(pre_save, sender=Task)
def update_notification_datetime(sender, instance, **kwargs):
    """
    This signal is used to update the notification_datetime field of a task
    if the task's notification_status changes to notified.
    """
    if instance.pk is None:  # Don't process for new instances
        return

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
