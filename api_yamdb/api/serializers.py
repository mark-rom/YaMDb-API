from datetime import datetime

from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import serializers

from reviews import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        exclude = ['id']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        exclude = ['id']


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = models.Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating')

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=models.Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=models.Genre.objects.all(),
        many=True,
        slug_field='slug'
    )

    class Meta:
        model = models.Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category')

    def validate_year(self, value):
        if value > datetime.today().year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли!'
            )
        return value


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
