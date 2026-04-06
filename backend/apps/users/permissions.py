from rest_framework.permissions import BasePermission

class IsMesero(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'mesero'

class IsBartender(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'bartender'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'