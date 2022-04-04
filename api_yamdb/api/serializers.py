from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews import models


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=models.Review.objects.all(),
                fields=('title_id', 'author')
            )
        ]

        def validate(self, data):
            """
            Проверка на наличие отзывов от этого пользователя на произведение.
            Пользователь может оставить
            только один отзыв на произведение.
            """
            title_reviews = get_object_or_404(
                models.Title, data['title_id']
            ).rewiews.all()
            author = self.context['request'].user
            if title_reviews.filter(author__in=author):
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв на это произведение'
                )
            return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'author', 'pub_date')
