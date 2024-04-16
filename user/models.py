from django.db import models
from django.contrib.auth.models import AbstractUser


class NilvaUser(AbstractUser):
    ADMIN = "admin"
    NORMAL = "normal"
    PERMISSION_CHOICES = [
        (ADMIN, "Admin"),
        (NORMAL, "Normal"),
    ]
    permissions = models.CharField(
        max_length=20, choices=PERMISSION_CHOICES, default=NORMAL
    )
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username}"
