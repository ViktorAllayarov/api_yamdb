from rest_framework import permissions

from users.models import RoleChoices


class IsAnonymous(permissions.BasePermission):
    """Класс реализует права только для неавторизованных пользователей."""

    message = "Ошибка: Пользователь не должен быть авторизован."

    def has_permission(self, request, view):
        return (
            request.user.is_anonymous
            or request.user.role == RoleChoices.ADMIN
            or request.user.is_staff
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Класс реализует права неавторизованным пользователям и выше - на чтение,
    администратору - не безопасные методы.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role == RoleChoices.ADMIN
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
            or request.user.role == RoleChoices.MODERATOR
            or request.user.role == RoleChoices.ADMIN
            or request.user.is_staff
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAuthorReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsAdmin(permissions.BasePermission):
    """Класс реализует права только для администраторов."""

    message = "Ошибка: Пользователь должен быть администратором."

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == RoleChoices.ADMIN or request.user.is_staff
        )
