from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from reviews import models
from . import serializers
from rest_framework import status


class UserCreateViewSet(generics.CreateAPIView):
    """
    Представление для создание пользователя. Имеет только POST запрос.
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.UserCreateSerializer
    queryset = models.User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = serializers.UserCreateSerializer(data=request.data)
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
    serializer_class = serializers.CustomTokenObtainSerializer
    queryset = models.User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = serializers.CustomTokenObtainSerializer(data=request.data)
        if serializer.is_valid():
            user = models.User.objects.get(
                username=serializer.data.get('username')
            )
            # Создаем токен для пользователя по переданному username
            token = serializer.get_token(user)
            return Response(
                {'Bearer': f"{ token['access'] }"},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
