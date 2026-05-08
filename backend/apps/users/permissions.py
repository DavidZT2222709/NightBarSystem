# apps/users/permissions.py  (Ajusta el nombre de la carpeta si es 'usuarios')
from rest_framework import permissions

class EsAdministrador(permissions.BasePermission):
    """
    Permite el acceso total solo a los administradores.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.rol and 
            request.user.rol.nombre == 'Administrador'
        )

class EsBartender(permissions.BasePermission):
    """
    Permite el acceso a los bartenders.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.rol and 
            request.user.rol.nombre == 'Bartender'
        )

class EsMesero(permissions.BasePermission):
    """
    Permite el acceso a los meseros.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.rol and 
            request.user.rol.nombre == 'Mesero'
        )

class EsMeseroOBartender(permissions.BasePermission):
    """
    Permiso combinado para que meseros y bartenders puedan ver catálogos.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated and request.user.rol):
            return False
        return request.user.rol.nombre in ['Mesero', 'Bartender']