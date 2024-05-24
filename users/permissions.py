from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsOwner(BasePermission):
    """Проверка прав доступа Пользователя (автора)"""
    message = "Доступно только Автору"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class IsSelf(BasePermission):
    """Проверка прав доступа Пользователя (автора)"""
    message = "Доступно только Владельцу"

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAdmin(BasePermission):
    """Проверка прав доступа группы Администраторов"""
    message = "Доступно только Администратору"

    def has_permission(self, request, view):
        return request.user.role == UserRoles.ADMIN
