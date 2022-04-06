from rest_framework import permissions

from reviews import models


class ReadOnly(permissions.BasePermission):
    """
    Базовый пермишен, разрешает безопасные запросы.
    """

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class IsAuthor(ReadOnly):
    """
    Дает полный доступ к Отзыву или Комментарию только авторам.
    Используется только в Review и Comment.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, models.Review) or isinstance(obj, models.Comment):
            return (
                request.user == obj.author
                or super().has_object_permission(request, view, obj)
            )

        return super().has_object_permission(request, view, obj)


class IsModer(ReadOnly):
    """
    Пользователь с ролью 'moderator' может править все Отзывы и Комментарии.
    Пользователь с ролью 'user' будет проверен на авторство.
    Используется только в Review и Comment,
    с другими объектами только на чтение.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_anonymous:
            if isinstance(obj, models.Review) or isinstance(obj, models.Comment):
                return (
                    request.user.role == 'moderator'
                    or super().has_object_permission(request, view, obj)
                )
            return super().has_object_permission(request, view, obj)

        return super().has_object_permission(request, view, obj)


class IsAdmin(ReadOnly):
    """
    Пользователь с ролью 'admin' вправе обращаться к любым эндпоинтам.
    В том числе делать небезопасные запросы.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_anonymous:
            return (
                request.user.role == 'admin'
                or super().has_object_permission(request, view, obj)
            )
        return super().has_object_permission(request, view, obj)


class IsSuperuser(ReadOnly):
    """
    Superuser вправе обращаться к любым эндпоинтам вне зависимости от role.
    В том числе делать небезопасные запросы.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_superuser
            or super().has_object_permission(request, view, obj)
        )
