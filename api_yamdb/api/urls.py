"""
Здесь будем использовать путь 'v1/',
чтобы при возможном расширении апи юзеры не потеряли свой текущий код.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('v1/', include(router.urls)),
]
