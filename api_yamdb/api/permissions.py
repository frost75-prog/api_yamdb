from rest_framework import permissions


class IsAccountAdminOrReadOnly(permissions.BasePermission):
    """
    Права администратора.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user.is_staff
