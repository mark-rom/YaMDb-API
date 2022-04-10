from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    viewsets, mixins, filters,
    generics, response, status
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
import rest_framework.permissions as rest_permissions

from reviews import models
from . import permissions
from . import serializers
from .filters import TitleFilterSet
from rest_framework.decorators import action


class CustomViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """Кастомный класс для чтения, создания и удаления объектов."""
    pass


class UserCreateViewSet(generics.CreateAPIView):
    """
    Представление для создания пользователя. Имеет только POST запрос.
    """
    permission_classes = (rest_permissions.AllowAny,)
    serializer_class = serializers.UserCreateSerializer
    queryset = models.User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = serializers.UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            serializer.send_mail(serializer.data['username'])

            return response.Response(
                data={
                    'email': serializer.data['email'],
                    'username': serializer.data['username']
                },
                status=status.HTTP_200_OK
            )

        return response.Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CustomTokenObtain(generics.CreateAPIView):
    """
    Представление для создания JWT токена. Имеет только POST запрос.
    """
    permission_classes = (rest_permissions.AllowAny,)
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


class UserViewSet(viewsets.ModelViewSet):
    """
    Вьюсет Пользователя.
    Реализованы методы чтения, создания,
    частичного обновления и удаления объектов.
    Есть поиск по полю username.
    """
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AdminOnly,)
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)

    @action(
        detail=False,
        methods=["get", "patch"],
        url_path="me",
        url_name="me",
        serializer_class=serializers.UserSerializer,
        permission_classes=(
            rest_permissions.IsAuthenticated,
        ),
    )
    def me(self, request):
        """
        Доступ пользователя к своей учетной записи по '/users/me/'.
        """
        me_user = request.user
        serializer = self.get_serializer(me_user)
        if request.method == "PATCH":
            serializer = self.get_serializer(
                me_user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(email=me_user.email, role=me_user.role)
            return response.Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CustomViewSet):
    """
    Вьюсет Категории.
    Реализованы методы чтения, создания и удаления объектов.
    Есть поиск по названию.
    """
    lookup_field = 'slug'
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CustomViewSet):
    """
    Вьюсет Жанры.
    Реализованы методы чтения, создания и удаления объектов.
    Есть поиск по названию.
    """
    lookup_field = 'slug'
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (permissions.AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вьюсет Произведения.
    Реализованы методы чтения, создания,
    частичного обновления и удаления объектов.
    Есть фильтр по полям slug категории/жанра, названию, году.
    """
    queryset = models.Title.objects.all()
    serializer_class = serializers.TitleReadSerializer
    permission_classes = (permissions.AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_сlass = TitleFilterSet

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.TitleReadSerializer
        return serializers.TitleWriteSerializer


class ReviewViewSet(ModelViewSet):
    """
    Вьюсет Отзывы.
    Реализованы методы чтения, создания,
    частичного обновления и удаления объектов.
    """
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        rest_permissions.IsAuthenticatedOrReadOnly,
        permissions.AuthorOrReadOnly
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
    """
    Вьюсет Комментарии.
    Реализованы методы чтения, создания,
    частичного обновления и удаления объектов.
    """
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        rest_permissions.IsAuthenticatedOrReadOnly,
        permissions.AuthorOrReadOnly
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
