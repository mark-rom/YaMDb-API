from rest_framework import serializers

from reviews.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('email', 'username',)

    def create(self, validated_data):
        # Использовать метод create_user, который мы
        # написали ранее, для создания нового пользователя.
        return User.objects.create_user(**validated_data)
