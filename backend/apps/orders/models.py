from django.db import models
from django.conf import settings

class Pedido(models.Model):
    ESTADOS_PEDIDO = [
        ('pending', 'Pendiente'),
        ('preparing', 'En Preparación'),
        ('delivered', 'Entregado'),
    ]

    mesa = models.ForeignKey('tables.Table', on_delete=models.CASCADE, related_name='pedidos')

    mesero = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null = True,
        related_name='pedidos_atendidos'
    )

    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='pending')

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido #{self.id} - Mesa {self.mesa} - {self.get.display()}"
    
    @property
    def total_pedido(self):
        return sum(detalle.subtotal for detalle in self.detalles.all())
    
class DetallePedido(models.Model):

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')

    producto = models.ForeignKey('products.Producto', on_delete=models.PROTECT)

    cantidad = models.PositiveIntegerField(default=1)

    # Guarda el precio unitario del producto al momento de la venta
    # que si el precio cambio altere los precios de las ventas anteriores

    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} (Pedido #{self.pedido.id})"

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario