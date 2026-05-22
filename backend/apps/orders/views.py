# apps/orders/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Q, F
from django.utils import timezone

# Importamos los modelos y serializadores
from .models import Pedido
from .serializers import PedidoSerializer

# Importamos los permisos de tu app de usuarios
from apps.users.permissions import EsMesero, EsBartender
from apps.products.models import Producto

class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated] # Base de seguridad: nadie sin token entra aquí

    def get_queryset(self):
        """
        ¡La magia de IroMarket ocurre aquí!
        El endpoint /api/orders/ devuelve datos diferentes dependiendo de QUIÉN pregunte.
        """
        user = self.request.user
        
        # 1. Vista del Bartender (RF-008: Cola FIFO)
        if user.rol.nombre == 'Bartender':
            today = timezone.localdate()
            return Pedido.objects.filter(
                Q(estado__in=['pending', 'preparing']) |
                Q(estado='delivered', creado_en__date=today)
            ).order_by('creado_en')
            
        # 2. Vista del Mesero
        elif user.rol.nombre == 'Mesero':
            # El mesero solo ve SUS propios pedidos.
            # .order_by('-creado_en') ordena del más nuevo al más viejo (LIFO) para que 
            # vea primero el pedido que acaba de enviar.
            return Pedido.objects.filter(mesero=user).order_by('-creado_en')
            
        # 3. Vista del Administrador
        elif user.rol.nombre == 'Administrador':
            # El Admin ve todo el historial para las estadísticas
            return Pedido.objects.all().order_by('-creado_en')

        # Por seguridad, si hay un rol fantasma, no devuelve nada
        return Pedido.objects.none()

    def get_permissions(self):
        """
        Restricciones estrictas por método HTTP.
        """
        if self.action == 'create':
            # Solo los meseros pueden generar comandas (POST)
            return [EsMesero()]
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        RF-004: Cuando el mesero crea el pedido desde la app React Native, 
        no necesita enviar su ID. Lo sacamos de su token JWT.
        """
        serializer.save(mesero=self.request.user)

    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        """
        Endpoint personalizado para que el Bartender cambie el estado con un simple botón.
        Ruta: PATCH /api/orders/{id_pedido}/cambiar_estado/
        Body: {"estado": "preparing"} o {"estado": "delivered"}
        """
        pedido = self.get_object()
        nuevo_estado = request.data.get('estado')
        user = request.user

        # Validar que el estado sea correcto
        if nuevo_estado not in ['pending', 'preparing', 'delivered']:
            return Response(
                {"error": "Estado no válido. Use 'pending', 'preparing' o 'delivered'."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Solo el Bartender (y el Admin en caso de emergencia) pueden cambiar estados
        if user.rol.nombre == 'Mesero':
            return Response(
                {"error": "Acceso denegado. Un mesero no puede despachar pedidos."},
                status=status.HTTP_403_FORBIDDEN
            )

        estado_anterior = pedido.estado

        with transaction.atomic():
            pedido.estado = nuevo_estado
            pedido.save()

            # Descontar stock solo al pasar a 'delivered' por primera vez
            if nuevo_estado == 'delivered' and estado_anterior != 'delivered':
                for detalle in pedido.detalles.all():
                    Producto.objects.filter(pk=detalle.producto_id).update(
                        stock=F('stock') - detalle.cantidad
                    )

        return Response({
            "message": "Estado del pedido actualizado correctamente",
            "pedido_id": pedido.id,
            "nuevo_estado": pedido.estado
        }, status=status.HTTP_200_OK)