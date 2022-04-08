from datetime import datetime

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from reviews import models


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя."""

    def send_mail(self, username):  # метод для отправки e-mail
        user = get_object_or_404(models.User, username=username)
        send_mail(
            'Добро пожаловать на YaMDB',
            f'Дорогой {username},\n'
            f'Ваш confirmation_code: {user.confirmation_code}',
            'from@example.com',
            [f'{user.email}'],
            fail_silently=False,
        )

    def validate(self, attrs):
        # Проверка ввода недопустимого имени ("me") и уникальность полей
        if attrs['username'] == 'me':
            raise serializers.ValidationError
        if attrs['username'] == attrs['email']:
            raise serializers.ValidationError(
                'Поля email и username не должны совпадать.')
        return attrs

    def create(self, validated_data):
        if 'role' not in self.initial_data:
            user = models.User.objects.create(**validated_data)
            return user

        if validated_data['role'] in ['moderator', 'admin']:
            return models.User.objects.create(**validated_data, is_staff=True)
        return super().create(validated_data)

    class Meta:
        model = models.User
        fields = ('email', 'username', 'role')


class CustomTokenObtainSerializer(serializers.ModelSerializer):
    """
    Кастомный сериализатор формы предоставления данных для аутентификации.
    Валидация по "confirmation_code".
    """
    username_field = models.User.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        # Переопределяем поля в форме получения токена
        super(CustomTokenObtainSerializer, self).__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields["confirmation_code"] = serializers.CharField()

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {'access': str(refresh.access_token), }

    def validate(self, attrs):
        user = get_object_or_404(models.User, username=attrs['username'])
        if attrs['confirmation_code'] != str(user.confirmation_code):
            raise serializers.ValidationError
        return attrs

    class Meta:
        model = models.User
        fields = ('confirmation_code', 'username', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        exclude = ['id']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        exclude = ['id']


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = models.Title
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
        queryset=models.Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=models.Genre.objects.all(),
        many=True,
        slug_field='slug'
    )

    class Meta:
        model = models.Title
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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(default=TitleReadSerializer)

    class Meta:
        model = models.Review
        fields = ('id', 'text', 'author', 'title', 'score', 'pub_date')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=models.Review.objects.all(),
                fields=['title', 'author'],
                message='вы уже оставляли отзыв'
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'author', 'pub_date')
