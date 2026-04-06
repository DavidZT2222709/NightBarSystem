# apps/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Columnas que se ven en la lista de usuarios
    list_display  = ['username', 'email', 'role', 'is_active']
    list_filter   = ['role', 'is_active']

    # Agregar el campo role al formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Rol en el sistema', {
            'fields': ('role',)
        }),
    )

    # Agregar el campo role al formulario de creación
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Rol en el sistema', {
            'fields': ('role',)
        }),
    )