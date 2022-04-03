from rest_framework import viewsets, mixins, filters
from reviews.models import Category, Genre, Title
from api.serializers import CategorySerializer, GenreSerializer
from api.serializers import TitleReadSerializer, TitleWriteSerializer
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import TitleFilterSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CustomViewSet):
    """Вью-класс Жанры. Реализованы методы чтения,
    создания и удаления объектов. Есть поиск по названию."""
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Вью-класс Произведения. Реализованы методы чтения,
    создания, частичного обновления и удаления объектов.
    Есть фильтр по полям slug категории/жанра, названию, году."""
    queryset = Title.objects.all()
    serializer_class = TitleReadSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_сlass = TitleFilterSet

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer
