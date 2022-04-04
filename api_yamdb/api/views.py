from django.core.mail import send_mail
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from reviews import models
from . import serializers
from rest_framework import status


class UserCreateViewSet(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserCreateSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        serializer = serializers.UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            confirmation_code = models.User.objects.get(
                username=username
            ).confirmation_code
            send_mail(
                'Добро пожаловать на YaMDB',
                f'Дорогой {username},'
                f'Ваш confirmation_code: {confirmation_code}',
                'from@example.com',  # Это поле "От кого"
                [f'{email}'],  # Это поле "Кому" (можно указать список)
                fail_silently=False,  # Сообщать об ошибках
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
