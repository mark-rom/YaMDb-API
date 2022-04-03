"""
Здесь будем использовать путь 'v1/',
чтобы при возможном расширении апи юзеры не потеряли свой текущий код.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.csrf import csrf_exempt
from .views import UserCreateViewSet

app_name = 'api'

router = DefaultRouter()
# router.register('auth/signup/', UserCreateViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', csrf_exempt(UserCreateViewSet)),
    # path(
    #     'v1/auth/token/',
    #     TokenObtainPairView.as_view(),
    #     name='token_obtain_pair'
    # ),
]
