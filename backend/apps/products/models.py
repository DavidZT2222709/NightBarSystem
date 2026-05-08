# apps/products/models.py
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    
    # Llave foránea a la categoría. Si se borra la categoría, protegemos los productos 
    # para no perder el historial de ventas.
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    
    # DecimalField es ideal para dinero. 
    # max_digits=10 y decimal_places=2 permite manejar precios altos en COP.
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Control de inventario básico
    stock = models.PositiveIntegerField(default=0)
    
    # Este campo es vital: permite al Administrador ocultar un producto temporalmente 
    # sin tener que borrarlo, ideal para cuando se acaba el insumo de un cóctel.
    disponible = models.BooleanField(default=True)
    
    # Opcional pero muy recomendado para la App Móvil del Mesero
    imagen = models.ImageField(upload_to='productos_img/', null=True, blank=True)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

    # Método útil para saber si se puede vender
    def se_puede_vender(self):
        return self.disponible and self.stock > 0