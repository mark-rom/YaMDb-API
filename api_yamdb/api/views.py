from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    viewsets, mixins, filters,
    generics, response, status
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from reviews import models
from . import permissions
from . import serializers
from .filters import TitleFilterSet


class UserCreateViewSet(generics.CreateAPIView):
    """
    Представление для создание пользователя. Имеет только POST запрос.
    """
    permission_classes = (AllowAny, )
    serializer_class = serializers.UserCreateSerializer
    queryset = models.User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = serializers.UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            serializer.send_mail(serializer.data['username'])

            return response.Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return response.Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CustomTokenObtain(generics.CreateAPIView):
    """
    Представление для создание JWT токена. Имеет только POST запрос.
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers.CustomTokenObtainSerializer
    queryset = models.User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = serializers.CustomTokenObtainSerializer(data=request.data)

        if serializer.is_valid():
            user = get_object_or_404(
                models.User,
                username=serializer.data['username']
            )

            token = serializer.get_token(user)

            return response.Response(
                {'token': f"{ token['access'] }"},
                status=status.HTTP_200_OK
            )

        return response.Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


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
        permissions.IsAdmin,
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
    permission_classes = (
        permissions.IsAdmin,
        permissions.IsSuperuser,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_сlass = TitleFilterSet

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.TitleReadSerializer
        return serializers.TitleWriteSerializer


class ReviewViewSet(ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        permissions.IsAuthor,
        permissions.IsModer,
        permissions.IsAdmin,
        permissions.IsSuperuser
    )

    def perform_create(self, serializer):
        """
        Поля author и title заполняются из данных запроса.
        """
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(
                models.Title,
                pk=self.kwargs.get('title_id')
            )
        )


class CommentViewSet(ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        permissions.IsAuthor,
        permissions.IsModer,
        permissions.IsAdmin,
        permissions.IsSuperuser
    )

    def perform_create(self, serializer):
        """
        Поля author и review заполняются из данных запроса.
        """
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(
                models.Review,
                pk=self.kwargs.get('review_id')
            )
        )
