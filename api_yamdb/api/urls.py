"""
Здесь будем использовать путь 'v1/',
чтобы при возможном расширении апи юзеры не потеряли свой текущий код.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
from api.views import UserCreateViewSet, CustomTokenObtain

app_name = 'api'

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'titles', TitleViewSet, basename='title')
# router.register(r'^auth/signup/$', UserCreateViewSet, basename='create_user')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', UserCreateViewSet.as_view()),
    path('v1/auth/token/', CustomTokenObtain.as_view()),
]
