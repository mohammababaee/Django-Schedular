from django.db import models
from user.models import NilvaUser


class Task(models.Model):
    NOT_NOTIFIED = "not_notified"
    NOTIFIED = "notified"
    NOTIFIED_CHOICES = [
        (NOT_NOTIFIED, "Not Notified"),
        (NOTIFIED, "Notified"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(NilvaUser, on_delete=models.CASCADE)
    due_datetime = models.DateTimeField(null=True, blank=True)
    # Define user notified status field with choices
    notification_status = models.CharField(
        max_length=20, choices=NOTIFIED_CHOICES, default=NOT_NOTIFIED
    )
    notification_datetime = models.DateTimeField(null=True, blank=True)
    # Tasks that need to be completed before this task
    pre_tasks = models.ManyToManyField("self", symmetrical=False, blank=True)

    def __str__(self):
        return f"Task {self.title} For {self.assigned_to}"
