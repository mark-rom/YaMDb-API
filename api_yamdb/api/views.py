from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from reviews import models
from . import serializers
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
    }


class UserCreateViewSet(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    # queryset = models.User.objects.all()
    serializer_class = serializers.UserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = serializers.UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer.send_mail(serializer.data['username'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtain(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.CustomTokenObtainSerializer
    queryset = models.User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = serializers.CustomTokenObtainSerializer(data=request.data)
        if serializer.is_valid():
            user = models.User.objects.get(
                username=serializer.data.get('username')
            )
            token = get_token_for_user(user)

            return Response(
                {'token': f"{ token['access'] }"},
                status=status.HTTP_200_OK
            )
        raise Exception('Все плохо')
