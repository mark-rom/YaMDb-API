from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre, User
from .serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        user_id = self.request.user
        serializer.save(author=get_object_or_404(User, pk=user_id))


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        user_id = self.request.user
        serializer.save(author=get_object_or_404(User, pk=user_id))
