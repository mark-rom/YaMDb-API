from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'useranme',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role'
    )
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'name',
        'slug'
    ]
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'name',
        'slug'
    ]
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'name',
        'year',
        'description',
        'genre',
        'category'
    ]
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'title_id',
        'text',
        'author',
        'score',
        'pub_date'
    ]
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'title_id',
        'review_id',
        'text',
        'author',
        'pub_date'
    ]
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
