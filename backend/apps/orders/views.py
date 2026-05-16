# apps/orders/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Importamos los modelos y serializadores
from .models import Pedido
from .serializers import PedidoSerializer

# Importamos los permisos de tu app de usuarios
from apps.users.permissions import EsMesero, EsBartender


class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retorna diferentes pedidos dependiendo del rol del usuario.
        """

        # 🔥 Evita errores cuando Swagger genera la documentación
        if getattr(self, 'swagger_fake_view', False):
            return Pedido.objects.none()

        user = self.request.user

        # 🔥 Seguridad extra
        if not user.is_authenticated:
            return Pedido.objects.none()

        # 🔥 Evita error si el usuario no tiene rol
        rol_nombre = getattr(user.rol, 'nombre', None)

        # 1. Vista del Bartender (FIFO)
        if rol_nombre == 'Bartender':

            return Pedido.objects.filter(
                estado__in=['pending', 'preparing']
            ).order_by('creado_en')

        # 2. Vista del Mesero
        elif rol_nombre == 'Mesero':

            return Pedido.objects.filter(
                mesero=user
            ).order_by('-creado_en')

        # 3. Vista del Administrador
        elif rol_nombre == 'Administrador':

            return Pedido.objects.all().order_by('-creado_en')

        # Rol desconocido
        return Pedido.objects.none()

    def get_permissions(self):
        """
        Restricciones estrictas por método HTTP.
        """

        if self.action == 'create':
            return [EsMesero()]

        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Asigna automáticamente el mesero desde el token JWT.
        """

        serializer.save(mesero=self.request.user)

    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        """
        PATCH /api/orders/{id}/cambiar_estado/

        Body:
        {
            "estado": "preparing"
        }
        """

        pedido = self.get_object()

        nuevo_estado = request.data.get('estado')

        user = request.user

        # 🔥 Seguridad extra
        if not user.is_authenticated:
            return Response(
                {"error": "Usuario no autenticado."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        rol_nombre = getattr(user.rol, 'nombre', None)

        # Validar estado
        if nuevo_estado not in ['pending', 'preparing', 'delivered']:

            return Response(
                {
                    "error": (
                        "Estado no válido. "
                        "Use 'pending', 'preparing' o 'delivered'."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # El mesero NO puede cambiar estados
        if rol_nombre == 'Mesero':

            return Response(
                {
                    "error": (
                        "Acceso denegado. "
                        "Un mesero no puede despachar pedidos."
                    )
                },
                status=status.HTTP_403_FORBIDDEN
            )

        pedido.estado = nuevo_estado
        pedido.save()

        return Response(
            {
                "message": "Estado del pedido actualizado correctamente",
                "pedido_id": pedido.id,
                "nuevo_estado": pedido.estado
            },
            status=status.HTTP_200_OK
        )