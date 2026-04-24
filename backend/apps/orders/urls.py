# apps/orders/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PedidoViewSet

# Creamos el router
router = DefaultRouter()

# Registramos el ViewSet de pedidos
# Esto creará rutas como /api/orders/ y /api/orders/{id}/
router.register(r'', PedidoViewSet, basename='pedidos')

urlpatterns = [
    # Incluye todas las rutas generadas por el router
    path('', include(router.urls)),
]