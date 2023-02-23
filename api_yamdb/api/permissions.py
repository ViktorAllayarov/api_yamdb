from rest_framework import permissions

from users.models import User


class IsAnonymous(permissions.BasePermission):
    """Класс реализует права только для неавторизованных пользователей."""

    message = "Ошибка: Пользователь не должен быть авторизован."

    def has_permission(self, request, view):
        return request.user.is_anonymous


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Класс реализует права неавторизованным пользователям и выше - на чтение,
    администратору - не безопасные методы.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == User.Role.ADMIN
            or request.user.is_staff
        )


class AuthorPlusOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.user.role == User.Role.MODERATOR
            or request.user.role == User.Role.ADMIN
            or request.user.is_staff
        )
