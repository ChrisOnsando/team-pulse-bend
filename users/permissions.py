from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permission to only allow admin users (is_staff=True) to access.
    """
    
    def has_permission(self, request, view):  # type: ignore[no-untyped-def]
        return request.user and request.user.is_staff
    