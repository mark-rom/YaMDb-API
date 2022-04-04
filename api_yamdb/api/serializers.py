from rest_framework import serializers

from reviews import models


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('email', 'username', )
