from rest_framework import serializers
from django.core.mail import send_mail
from reviews import models
from django.shortcuts import get_object_or_404
# from rest_framework.response import Response
# from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя."""

    def send_mail(self, username):  # метод для отправки e-mail
        user = get_object_or_404(models.User, username=username)
        send_mail(
            'Добро пожаловать на YaMDB',
            f'Дорогой {username},'
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
        model = models.User
        fields = ('email', 'username', )


class CustomTokenObtainSerializer(serializers.Serializer):
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
        # Метод для создания токена
        refresh = RefreshToken.for_user(user)
        return {'access': str(refresh.access_token), }

    def validate(self, attrs):
        user = get_object_or_404(models.User, username=attrs['username'])
        if attrs['confirmation_code'] != user.confirmation_code:
            raise serializers.ValidationError
        return attrs

    class Meta:
        model = models.User
        fields = ('confirmation_code', 'username', )
