# from django.shortcuts import render
# from django.core.mail import send_mail
from rest_framework import generics
from rest_framework import permissions
from reviews import models
from . import serializers

# send_mail(
#     'Тема письма',
#     'Текст письма.',
#     'from@example.com',  # Это поле "От кого"
#     ['to@example.com'],  # Это поле "Кому" (можно указать список адресов)
#     fail_silently=False,  # Сообщать об ошибках («молчать ли об ошибках?»)
# )


class UserCreateViewSet(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserCreateSerializer
    permission_classes = (permissions.AllowAny, )
