from rest_framework import permissions


class IsAccountAdminOrReadOnly(permissions.BasePermission):
    """
    Права администратора, или только безопасные запросы.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin)


class IsAdmin(permissions.BasePermission):
    """
    Права администратора.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Доступ только для автора или только для чтения"""
    def has_object_permission(self, request, view, obj):
        # print('1', request.user.is_moderator, '2', request.user.is_admin)
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_moderator or request.user.is_admin:
            return True
        return obj.author == request.user


class IsAuthorOrAdministratorOrReadOnly(permissions.BasePermission):
    """
    Права автора или администратора.
    Доступны безопасные методы HTTP.
    """
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)
