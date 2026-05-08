# apps/usuarios/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rol

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    # Columnas que se mostrarán en la tabla principal del panel
    list_display = ('email', 'nombre', 'rol', 'is_active', 'is_staff')
    
    # Campos por los que el Administrador podrá buscar
    search_fields = ('email', 'nombre', 'username')
    
    # Filtros laterales
    list_filter = ('rol', 'is_active', 'is_staff')
    
    # Organización visual de los campos al editar/crear un usuario
    fieldsets = (
        ('Credenciales', {'fields': ('email', 'password')}),
        ('Información Personal', {'fields': ('nombre', 'username', 'numero_telefono', 'rol')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información de IroMarket', {
            'fields': ('email', 'nombre', 'numero_telefono', 'rol'),
        }),
    )

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    # Muestra el ID y el nombre para que sea más fácil de gestionar
    list_display = ('id', 'nombre')

# Personalización del sitio de administración adaptado a tu proyecto
admin.site.site_header = "Administración de IroMarket"
admin.site.site_title = "Panel de Control IroMarket"
admin.site.index_title = "Bienvenido al Sistema de Gestión IroMarket"