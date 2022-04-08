from django.contrib import admin
from .models import Category, Comment, Genre, Review, Title, TitleGenre, User
from django.contrib.auth.admin import UserAdmin
from reviews.forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = [
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role'
    ]
    empty_value_display = '-пусто-'


class TitleGenreInline(admin.TabularInline):
    model = TitleGenre


class GenreAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'name',
        'slug'
    ]
    inlines = (TitleGenreInline,)
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
        'category'
    ]
    inlines = (TitleGenreInline,)
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
        'review_id',
        'text',
        'author',
        'pub_date'
    ]
    empty_value_display = '-пусто-'


admin.site.register(User, CustomUserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
