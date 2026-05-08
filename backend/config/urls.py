from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Importaciones para Swagger (Documentación Interactiva)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuración de la vista de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="IroMarket API",
        default_version='v1',
        description="Sistema de gestión de pedidos para disco-bares en Bucaramanga",
        contact=openapi.Contact(email="soporte@iromarket.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # 1. Panel de Administración de Django
    path('admin/', admin.site.urls),

    # 2. Endpoints de la Aplicación Usuarios (Auth, Roles, Registro)
    path('api/users/', include('apps.users.urls')),

    # 3. Endpoints de la Aplicación Mesas (Disponibilidad)
    path('api/tables/', include('apps.tables.urls')),

    # 4. Endpoints de la Aplicación Productos (Catálogo e Inventario)
    path('api/products/', include('apps.products.urls')),

    # 5. Endpoints de la Aplicación Pedidos (Cola FIFO para Bartender)
    path('api/orders/', include('apps.orders.urls')),

    # 6. Endpoints de la Aplicación Estadísticas (Cortes de Caja)
    path('api/stats/', include('apps.stats.urls')),

    # 7. Documentación de la API (Swagger y ReDoc)
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Configuración para servir archivos MEDIA (Imágenes de productos) en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)