from rest_framework import permissions

from reviews import models


class ListReadOnly(permissions.BasePermission):
    """
    Базовый пермишен, разрешает только безопасные запросы к спискам.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class ObjectReadOnly(permissions.BasePermission):
    """
    Базовый пермишен, разрешает только безопасные запросы к объектам.
    """
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class ListObjectReadOnly(ListReadOnly, ObjectReadOnly):
    """
    Базовый пермишен, разрешает только безопасные запросы к спискам и объектам.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class AuthorOrReadOnly(ObjectReadOnly):
    """
    Дает право изменять и удалять объект Отзыва или Комментария только автору.
    Используется только в ReviewViewSet и CommentViewSet.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.author
            or super().has_object_permission(request, view, obj)
        )


class ModerOrReadOnly(ObjectReadOnly):
    """
    Пользователь с ролью 'moderator' может править все Отзывы и Комментарии.
    Используется только в Review и Comment,
    с другими объектами только чтение.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if isinstance(obj, models.Review) or isinstance(obj, models.Comment):
            return (
                (user.is_authenticated and user.role == 'moderator')
                or super().has_object_permission(request, view, obj)
            )

        return super().has_object_permission(request, view, obj)


class AdminOnly(permissions.BasePermission):
    """
    Пермишен для доступа к /users/
    """

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_superuser
            or (user.is_authenticated and user.role == 'admin')
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_superuser
            or (user.is_authenticated and user.role == 'admin')
        )


class AdminOrReadOnly(ListObjectReadOnly):
    """
    Пермишен для доступа к /categories/, /genres/ и /titles/.
    """
    def has_permission(self, request, view):
        user = request.user
        return (
            (user.is_authenticated and user.role == 'admin')
            or request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            (user.is_authenticated and user.role == 'admin')
            or request.method in permissions.SAFE_METHODS
        )
