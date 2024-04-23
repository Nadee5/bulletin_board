from rest_framework.permissions import BasePermission

from users.models import UserRoles


class IsOwner(BasePermission):
    """Проверка прав доступа Пользователя (автора)"""
    message = "Доступно только владельцу"

    def has_object_permission(self, request, view, obj):
        return request.user.email == obj.email

    # def has_permission(self, request, view): # для просмотра только своего профиля
    #     return request.user ==


class IsAdmin(BasePermission):
    """Проверка прав доступа группы Администраторов"""
    message = "Доступно группе Администраторов"

    def has_permission(self, request, view):
        return request.user.role == UserRoles.ADMIN
