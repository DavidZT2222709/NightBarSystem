from django.db import models

class Table(models.Model):
    ESTADOS_MESA = [
        ('available', 'Disponible'),
        ('occupied', 'Ocupada'),
    ]

    numero = models.PositiveIntegerField(unique=True)

    capacidad = models.PositiveIntegerField(default=4)

    estado = models.CharField(max_length=20, choices=ESTADOS_MESA, default='available')

    def __str__(self):
        return f"Mesa {self.numero} - {self.get.estado_display()}"
    
    