# apps/orders/apps.py
from django.apps import AppConfig

class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.orders'
    # Nombre legible en el panel de administración
    verbose_name = 'Operaciones de Barra e IroMarket'