from rest_framework import permissions


class CurrentUserOrAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Пермишн для Пользователя. Djoser"""

    def has_object_permission(self, request, view, obj):
        user = request.user
        if type(obj) is type(user) and obj == user:
            return True
        return request.method in permissions.SAFE_METHODS or user.is_staff


class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Доступно Автору или для чтения"""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
