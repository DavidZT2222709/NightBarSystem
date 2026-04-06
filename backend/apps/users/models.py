from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        MESERO = 'mesero', 'Mesero'
        BARTENDER = 'bartender', 'Bartender'
        ADMIN = 'admin', 'Administrador'

    role = models.CharField(max_length=20, choices=Role.choices)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True
    )


    def __str__(self):
        return f"{self.username} ({self.role})"
