from rest_framework import serializers
from reviews.models import Category, Genre, Title, User
from datetime import datetime
from django.db.models import Avg
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя."""

    def send_mail(self, username):  # метод для отправки e-mail
        user = get_object_or_404(User, username=username)
        send_mail(
            'Добро пожаловать на YaMDB',
            f'Дорогой {username}, '
            f'Ваш confirmation_code: {user.confirmation_code}',
            'from@example.com',  # Это поле "От кого"
            [f'{user.email}'],  # Это поле "Кому" (можно указать список)
            fail_silently=False,  # Сообщать об ошибках
        )

    def validate(self, attrs):
        # Проверка юзера на наличие в таблице уже есть
        if attrs['username'] == 'me':
            raise serializers.ValidationError
        if attrs['username'] == attrs['email']:
            raise serializers.ValidationError(
                'Поля email и username не должны совпадать.')
        return attrs

    class Meta:
        model = User
        fields = ('email', 'username', )


class CustomTokenObtainSerializer(serializers.Serializer):
    """
    Кастомный сериализатор формы предоставления данных для аутентификации.
    Валидация по "confirmation_code".
    """
    username_field = User.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        # Переопределяем поля в форме получения токена
        super(CustomTokenObtainSerializer, self).__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields["confirmation_code"] = serializers.CharField()

    def get_token(self, user):
        # Метод для создания токена
        refresh = RefreshToken.for_user(user)
        return {'access': str(refresh.access_token), }

    class Meta:
        model = User
        fields = ('confirmation_code', 'username', )

        def validate(self, attrs):
            user = get_object_or_404(User, username=attrs['username'])
            if attrs['confirmation_code'] != user.confirmation_code:
                raise serializers.ValidationError
            return attrs


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ['id']


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating')

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category')

    def validate_year(self, value):
        if value > datetime.today().year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли!'
            )
        return value
