from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from reviews import models
from .serializers import ReviewSerializer, CommentSerializer
from . import permissions


class ReviewViewSet(ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthor,
        permissions.IsModer,
        permissions.IsAdmin,
        permissions.IsSuperuser
    )

    def perform_create(self, serializer):
        """
        Поля author и title заполняются из данных запроса.
        """
        author = get_object_or_404(models.User, pk=self.request.user)
        title = get_object_or_404(models.Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=author, title_id=title)


class CommentViewSet(ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthor,
        permissions.IsModer,
        permissions.IsAdmin,
        permissions.IsSuperuser
    )

    def perform_create(self, serializer):
        """
        Поля author, title и review заполняются из данных запроса.
        """
        author = get_object_or_404(models.User, pk=self.request.user)
        title = get_object_or_404(models.Title, pk=self.kwargs.get('title_id'))
        review = get_object_or_404(
            models.Review, pk=self.kwargs.get('review_id')
        )
        serializer.save(author=author, title_id=title, review_id=review)
