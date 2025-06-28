from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Allows access only to users with 'admin' role.
    Assumes user has a related 'role' object with 'name' field.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user.role, 'name', '').lower() == 'admin'