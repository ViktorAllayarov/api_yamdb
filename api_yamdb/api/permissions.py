from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
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


class AuthorModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
        )


class IsAdmin(permissions.BasePermission):
    """Класс реализует права только для администраторов."""

    message = "Ошибка: Пользователь должен быть администратором."

    def has_permission(self, request, view):
        print(111111111111111111111111)
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            print(request.user.is_admin)
        return (request.user.is_authenticated and request.user.is_admin)
