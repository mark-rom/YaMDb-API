from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Genre, Title
from datetime import datetime


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ['id']
        validators = [
            UniqueValidator(
                queryset=Category.objects.all(),
                fields=['slug']
            )
        ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        exclude = ['id']
        validators = [
            UniqueValidator(
                queryset=Genre.objects.all(),
                fields=['slug']
            )
        ]


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        read_only=True,
        queryset=Category.objects.all()
    )
    genre = GenreSerializer(
        read_only=True,
        many=True,
        queryset=Genre.objects.all()
    )
    rating = serializers.IntegerField(
        read_only=True,
        required=False
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating')

    def validate_year(self, value):
        if value > datetime.today().year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли!'
            )
        return value
