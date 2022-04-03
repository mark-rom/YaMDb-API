"""
Здесь будем использовать путь 'v1/',
чтобы при возможном расширении апи юзеры не потеряли свой текущий код.
"""

from django.urls import path, include
from rest_framework import routers
# from rest_framework_simplejwt.views import TokenObtainPairView
# from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'api'

router = routers.DefaultRouter()
# router.register(r'auth/signup/', UserCreateViewSet, basename='create_user')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', views.UserCreateViewSet.as_view()),
    # path(
    #     'v1/auth/token/',
    #     TokenObtainPairView.as_view(),
    #     name='token_obtain_pair'
    # ),
]
