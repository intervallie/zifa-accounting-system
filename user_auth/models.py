from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserAccount(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    )

    role = models.CharField(choices=ROLE_CHOICES, default='staff', max_length=10)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.is_superuser:
                self.role = 'admin'
            super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    