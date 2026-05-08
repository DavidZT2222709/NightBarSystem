# apps/orders/admin.py
from django.contrib import admin
from .models import Pedido, DetallePedido

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0 # No mostrar filas vacías por defecto
    readonly_fields = ('subtotal',)
    # Evita que se borren detalles de pedidos ya cerrados por accidente
    can_delete = False 

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    # Columnas principales
    list_display = ('id', 'mesa', 'mesero', 'estado', 'total_pedido', 'creado_en')
    
    # Filtros para auditoría rápida
    list_filter = ('estado', 'creado_en', 'mesero')
    
    # Búsqueda por mesa o ID
    search_fields = ('id', 'mesa__numero', 'mesero__nombre')
    
    # Integración de los detalles dentro de la vista del pedido
    inlines = [DetallePedidoInline]
    
    # Colores o iconos para el estado (opcional pero muy útil)
    list_editable = ('estado',) # Permite al admin corregir estados desde la lista

    def total_pedido(self, obj):
        return f"${obj.total_pedido:,.2f}"
    total_pedido.short_description = "Total COP"