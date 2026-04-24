# apps/products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet, CategoriaViewSet

# Creamos el router y registramos los ViewSets
router = DefaultRouter()
router.register(r'catalogo', ProductoViewSet, basename='productos')
router.register(r'categorias', CategoriaViewSet, basename='categorias')

urlpatterns = [
    # Incluye todas las rutas generadas por el router
    path('', include(router.urls)),
]