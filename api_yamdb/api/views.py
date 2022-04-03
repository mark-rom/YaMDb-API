from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from reviews import models
from .serializers import ReviewSerializer, CommentSerializer
import permissions


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
        user_id = self.request.user
        serializer.save(author=get_object_or_404(models.User, pk=user_id))


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
        user_id = self.request.user
        serializer.save(author=get_object_or_404(models.User, pk=user_id))
