from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Categoria, Producto
from .serializers import CategoriaSerializer, ProductoSerializer

from apps.users.permissions import EsAdministrador

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    """
    Función para que el administrador tenga los siguientes permisos:
    - Crear, Actualizar y Eliminar
    - Ver (list/retriever): Cualquier usuario autenticado (Mesero, Bartender)
    """
    def get_permissions(self):

        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [EsAdministrador()]
        return [IsAuthenticated()]
    
    def get_queryset(self):

        user = self.request.user
        if user.is_authenticated and user.rol.nombre != 'Administrador':
            return Producto.objects.filter(disponible=True)
        return Producto.objects.all()
    
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [EsAdministrador()]
        return [IsAuthenticated()]