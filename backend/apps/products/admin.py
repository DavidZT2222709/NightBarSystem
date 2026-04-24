from django.contrib import admin
from .models import Categoria, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'disponible', 'categoria')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre',)
    list_editable = ('precio', 'stock', 'disponible') # Permite editar rápido desde la lista