from django.db import models
from apps.users.models import User
from apps.tables.models import Table
from apps.products.models import Product

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING   = 'pending',   'Pendiente'
        PREPARING = 'preparing', 'En preparación'
        DELIVERED = 'delivered', 'Entregado'

    mesero     = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders')
    table      = models.ForeignKey(Table, on_delete=models.PROTECT, related_name='orders')
    status     = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  # FIFO automático para el bartender

    def __str__(self):
        return f"Mesa {self.table.number} - {self.status}"


class OrderItem(models.Model):
    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"