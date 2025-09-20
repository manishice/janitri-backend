from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminRole(BasePermission):
    """Allow only admin role."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ADMIN"


class IsSelfOrAdmin(BasePermission):
    """Allow user to access their own record, or admin to access any."""
    def has_object_permission(self, request, view, obj):
        return request.user.role == "ADMIN" or obj == request.user
