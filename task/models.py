from django.db import models
from user.models import User

class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    time_to_send = models.DateTimeField(null=True, blank=True, default=None)
    # Tasks that need to be completed before this task
    pre_tasks = models.ManyToManyField('self', symmetrical=False, blank=True)
