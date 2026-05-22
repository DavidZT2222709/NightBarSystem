# apps/stats/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum, Count, F
from django.db.models.functions import Coalesce

from .models import ReporteDiario
from .serializers import ReporteDiarioSerializer
from apps.users.permissions import EsAdministrador
from apps.orders.models import Pedido, DetallePedido

class ReporteDiarioViewSet(viewsets.ModelViewSet):
    # Ordenamos del reporte más reciente al más antiguo
    queryset = ReporteDiario.objects.all().order_by('-fecha')
    serializer_class = ReporteDiarioSerializer
    
    # Nadie más que el 'jefe final' (Admin) debería ver la plata del negocio
    permission_classes = [EsAdministrador] 

    @action(detail=False, methods=['post'])
    def generar_corte_hoy(self, request):
        """
        Calcula las métricas del día actual y las consolida en la tabla de estadísticas.
        """
        hoy = timezone.localdate()

        # 1. Calcular Ingresos Totales de hoy
        ingresos = Pedido.objects.filter(
            estado='delivered', creado_en__date=hoy
        ).aggregate(
            total=Sum(F('detalles__cantidad') * F('detalles__precio_unitario'))
        )['total'] or 0

        # 2. Total de pedidos
        pedidos_totales = Pedido.objects.filter(estado='delivered', creado_en__date=hoy).count()

        # 3. Producto Estrella (El más vendido)
        top_producto = DetallePedido.objects.filter(
            pedido__estado='delivered', pedido__creado_en__date=hoy
        ).values('producto__nombre').annotate(
            vendidos=Sum('cantidad')
        ).order_by('-vendidos').first()
        
        nombre_top_producto = top_producto['producto__nombre'] if top_producto else "Ninguno"

        # 4. Mesero MVP — usa nombre si está definido, si no cae a username
        top_mesero = Pedido.objects.filter(
            estado='delivered', creado_en__date=hoy
        ).annotate(
            nombre_display=Coalesce('mesero__nombre', 'mesero__username')
        ).values('nombre_display').annotate(
            atendidos=Count('id')
        ).order_by('-atendidos').first()

        nombre_top_mesero = top_mesero['nombre_display'] if top_mesero else "Ninguno"

        # 5. Guardar el "Save State" en la base de datos
        # update_or_create permite que si el admin presiona el botón dos veces por error, 
        # simplemente actualice los datos de hoy en lugar de crear un reporte duplicado.
        reporte, created = ReporteDiario.objects.update_or_create(
            fecha=hoy,
            defaults={
                'ingresos_totales': ingresos,
                'pedidos_completados': pedidos_totales,
                'producto_estrella': nombre_top_producto,
                'mesero_destacado': nombre_top_mesero
            }
        )

        return Response({
            "mensaje": "¡Corte de caja guardado con éxito!",
            "reporte": ReporteDiarioSerializer(reporte).data
        }, status=status.HTTP_200_OK)