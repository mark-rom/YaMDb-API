from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews import models
from . import permissions
from . import serializers
from .filters import TitleFilterSet


class CustomViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """Кастомный класс для чтения, создания и удаления объектов."""
    pass


class CategoryViewSet(CustomViewSet):
    """Вью-класс Категории. Реализованы методы чтения,
    создания и удаления объектов. Есть поиск по названию."""
    lookup_field = 'slug'
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        permissions.IsAdmin,
        permissions.IsSuperuser
    )
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CustomViewSet):
    """Вью-класс Жанры. Реализованы методы чтения,
    создания и удаления объектов. Есть поиск по названию."""
    lookup_field = 'slug'
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        permissions.IsAdmin,
        permissions.IsSuperuser
    )
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Вью-класс Произведения. Реализованы методы чтения,
    создания, частичного обновления и удаления объектов.
    Есть фильтр по полям slug категории/жанра, названию, году."""
    queryset = models.Title.objects.all()
    serializer_class = serializers.TitleReadSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_сlass = TitleFilterSet

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.TitleReadSerializer
        return serializers.TitleWriteSerializer


class ReviewViewSet(ModelViewSet):
    # к /reviews/ должен выводиться список
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        permissions.IsAuthor,
        permissions.IsModer,
        permissions.IsAdmin,
        permissions.IsSuperuser
    )

    def perform_create(self, serializer):
        """
        Поля author и title заполняются из данных запроса.
        """
        author = get_object_or_404(models.User, pk=self.request.user)
        title = get_object_or_404(models.Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=author, title_id=title)


class CommentViewSet(ModelViewSet):
    # к /comments/ должен выводиться список
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        permissions.IsAuthor,
        permissions.IsModer,
        permissions.IsAdmin,
        permissions.IsSuperuser
    )

    def perform_create(self, serializer):
        """
        Поля author, title и review заполняются из данных запроса.
        """
        author = get_object_or_404(models.User, pk=self.request.user)
        title = get_object_or_404(models.Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(
            models.Review, pk=self.kwargs.get('review_id')
        )
        serializer.save(author=author, title_id=title, review_id=review)
