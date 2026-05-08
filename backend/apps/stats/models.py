# apps/stats/models.py
from django.db import models

class ReporteDiario(models.Model):
    # La fecha del reporte (ej. 2026-04-23)
    fecha = models.DateField(unique=True)
    
    # El dinero total generado ese día
    ingresos_totales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Cuántas comandas se entregaron con éxito
    pedidos_completados = models.PositiveIntegerField(default=0)
    
    # Podemos guardar el nombre del producto estrella del día como texto plano
    producto_estrella = models.CharField(max_length=200, null=True, blank=True)
    
    # El mesero que más pedidos entregó (el MVP del día)
    mesero_destacado = models.CharField(max_length=150, null=True, blank=True)

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Corte de Caja: {self.fecha} - ${self.ingresos_totales}"