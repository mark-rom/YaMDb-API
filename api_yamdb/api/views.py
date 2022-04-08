from rest_framework import viewsets, mixins, filters, generics, status
from rest_framework.response import Response
from reviews.models import Genre, Category, Title, User
from api.serializers import CategorySerializer, GenreSerializer
from api.serializers import TitleReadSerializer, TitleWriteSerializer
from api.serializers import UserCreateSerializer, CustomTokenObtainSerializer
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import TitleFilterSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import permissions


class UserCreateViewSet(generics.CreateAPIView):
    """
    Представление для создание пользователя. Имеет только POST запрос.
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Отправляем письмо на почту
            serializer.send_mail(serializer.data['username'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtain(generics.CreateAPIView):
    """
    Представление для создание JWT токена. Имеет только POST запрос.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomTokenObtainSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(
                username=serializer.data.get('username')
            )
            # Создаем токен для пользователя по переданному username
            token = serializer.get_token(user)
            return Response(
                {'Bearer': f"{ token['access'] }"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


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
