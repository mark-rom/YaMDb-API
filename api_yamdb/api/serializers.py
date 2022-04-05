from rest_framework import serializers
from django.core.mail import send_mail
from reviews import models
from django.shortcuts import get_object_or_404


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
        super(CustomTokenObtainSerializer, self).__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields["confirmation_code"] = serializers.CharField()

    class Meta:
        model = models.User
        fields = ('confirmation_code', 'username', )

        def validate(self, attrs):
            user = models.User.objects.get(username=attrs['username'])
            if attrs['confirmation_code'] == user.confirmation_code:
                return attrs
