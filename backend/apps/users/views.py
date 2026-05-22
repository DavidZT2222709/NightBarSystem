# apps/usuarios/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from .models import Usuario, Rol
from .serializers import (
    RegisterUserSerializer, 
    UserSerializer, 
    RolSerializer, 
    CustomTokenObtainPairSerializer
)

User = get_user_model()


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer
    
    # Asignación dinámica de permisos según la acción
    def get_permissions(self):
        if self.action in ('registro', 'por_rol'):
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['put'])
    def toggle_active(self, request, pk=None):
        try:
            usuario = self.get_object()
            
            # Alternar el estado activo
            usuario.is_active = not usuario.is_active
            usuario.save()  # Guarda en BD

            return Response(
                {"message": "Estado actualizado", "is_active": usuario.is_active},
                status=status.HTTP_200_OK
            )

        except Usuario.DoesNotExist:
            return Response(
                {"error": "Usuario no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
    @action(detail=False, methods=['get'], url_path='por_rol')
    def por_rol(self, request):
        rol_nombre = request.query_params.get('rol')
        if not rol_nombre:
            return Response({'error': "Parámetro 'rol' requerido"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            rol = Rol.objects.get(nombre=rol_nombre)
        except Rol.DoesNotExist:
            return Response({'error': 'Rol no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        usuarios = Usuario.objects.filter(rol=rol, is_active=True).values('id', 'email', 'nombre', 'username')
        return Response(list(usuarios))

    # Acción personalizada para el registro: Crea el endpoint /usuarios/registro/
    @action(detail=False, methods=['post'])
    def registro(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Cambiamos a ReadOnlyModelViewSet para proteger los roles base de IroMarket
class RolViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint de solo lectura. 
    Permite listar (GET /roles/) y ver detalle (GET /roles/id/).
    No permite POST, PUT, ni DELETE.
    """
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [AllowAny] # Permite que el formulario de registro frontend pueda consultar los roles disponibles


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer