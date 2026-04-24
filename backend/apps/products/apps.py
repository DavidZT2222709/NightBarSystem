# apps/products/apps.py
from django.apps import AppConfig

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # Asegúrate de que coincida con la estructura de tus carpetas
    name = 'apps.products' 
    verbose_name = 'Gestión de Inventario IroMarket'