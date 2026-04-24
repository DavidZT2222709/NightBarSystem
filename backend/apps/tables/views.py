# apps/tables/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Table
from .serializers import TableSerializer
from apps.users.permissions import EsAdministrador

class TableViewSet(viewsets.ModelViewSet):
    # Ordenamos por número de mesa para que la app del mesero se vea organizada
    queryset = Table.objects.all().order_by('numero')
    serializer_class = TableSerializer

    def get_permissions(self):
        """
        Crear o eliminar mesas es tarea exclusiva del Administrador.
        Ver las mesas (GET) está permitido para cualquier empleado autenticado.
        """
        if self.action in ['create', 'destroy']:
            return [EsAdministrador()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        """
        Endpoint rápido para la App React Native del Mesero.
        Ruta: PATCH /api/tables/{id_mesa}/cambiar_estado/
        Body: {"estado": "occupied"}
        """
        mesa = self.get_object()
        nuevo_estado = request.data.get('estado')
        user = request.user

        if nuevo_estado not in ['available', 'occupied']:
            return Response(
                {"error": "Estado no válido. Use 'available' o 'occupied'."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Solo Meseros y Administradores pueden ocupar/liberar mesas
        if user.rol.nombre not in ['Mesero', 'Administrador']:
            return Response(
                {"error": "Acceso denegado. Un bartender no gestiona mesas."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        mesa.estado = nuevo_estado
        mesa.save()
        
        return Response({
            "message": "Estado de la mesa actualizado",
            "mesa": mesa.numero,
            "nuevo_estado": mesa.estado
        }, status=status.HTTP_200_OK)