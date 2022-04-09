"""
Здесь будем использовать путь 'v1/',
чтобы при возможном расширении апи юзеры не потеряли свой текущий код.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'genres', views.GenreViewSet, basename='genre')
router.register(r'titles', views.TitleViewSet, basename='title')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', views.UserCreateViewSet.as_view()),
    path('v1/auth/token/', views.CustomTokenObtain.as_view()),
]
