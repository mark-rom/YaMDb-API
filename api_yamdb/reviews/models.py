import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE_CHOISES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)

SCORE_CHOISES = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10)
]


class User(AbstractUser):
    email = models.EmailField(
        blank=False, null=False,
        unique=True, max_length=254
    )
    password = models.CharField(blank=True, null=True, max_length=128)
    first_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(choices=ROLE_CHOISES, default='user', max_length=9)
    confirmation_code = models.CharField(
        default=uuid.uuid4,
        editable=True,
        unique=True,
        max_length=36,
        auto_created=True
    )

    REQUIRED_FIELDS = ['email', ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_login_fields',

            ),
        ]

    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField(
        help_text='Нельзя добавлять произведения, которые еще не вышли'
    )
    description = models.TextField(blank=True, null=True)  # Убрать перед ревью
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        db_column='genre'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        db_column='category',
        null=True,
        related_name='categories'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        db_column='title',
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='author',
        related_name='reviews'
    )
    score = models.IntegerField(choices=SCORE_CHOISES)
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_review'
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        db_column='review',
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='author',
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        db_column='title',
        related_name='title'
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL,
        db_column='genre',
        null=True,
        related_name='genre')

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'

    def __str__(self):
        return f'{self.title} {self.genre}'
