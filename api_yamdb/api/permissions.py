from rest_framework import permissions


class IsAnonymous(permissions.BasePermission):
    """Класс реализует права только для неавторизованных пользователей."""

    message = 'Ошибка: Пользователь не должен быть авторизован.'

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsAuthorReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
