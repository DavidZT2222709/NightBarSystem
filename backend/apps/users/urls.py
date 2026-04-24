from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

# Asegúrate de importar CustomTokenObtainPairView
from .views import UsuarioViewSet, RolViewSet, CustomTokenObtainPairView

# Rutas del router (usuarios y roles)
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
router.register(r'roles', RolViewSet, basename='roles')

urlpatterns = [
    # Endpoints generados por el router (/usuarios/ y /roles/)
    path('', include(router.urls)),

    # Endpoints de Autenticación JWT para IroMarket
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]