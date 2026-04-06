from django.db import models

# Create your models here.
class Table(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Disponible'
        OCCUPIED = 'occupied', 'Ocupadad'

    number = models.PositiveBigIntegerField(unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)

    def __str__(self):
        return f"Mesa {self.number} - {self.Status}"