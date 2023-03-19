from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import User


HEADER_LENGTH = 50
SCORE_MIN = 1
SCORE_MAX = 10
CHOICES = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']


class Category(models.Model):
    """
    Категории (типы) произведений («Фильмы», «Книги», «Музыка»).
    Одно произведение может быть привязано только к одной категории.
    """
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
        help_text='Введите название категории',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name='Слаг-индентификатор',
        help_text='Введите slug-идентификатор',
    )
    objects = models.Manager()

    class Meta:
        """Метаданные."""
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'

    def __str__(self):
        return str(self.name)[:HEADER_LENGTH]


class Genre(models.Model):
    """
    Жанры произведений.
    Одно произведение может быть привязано к нескольким жанрам.
    """
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
        help_text='Введите название жанра',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name='Слаг-индентификатор',
        help_text='Введите slug-идентификатор',
    )
    objects = models.Manager()

    class Meta:
        """Метаданные."""
        verbose_name_plural = 'Жанры'
        verbose_name = 'Жанр'

    def __str__(self):
        return str(self.name)[:HEADER_LENGTH]


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы,
    (определённый фильм, книга или песенка).
    """
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Введите название произведения',
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        help_text='Введите год выпуска произведения',
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория произведения',
        help_text='Выберите категорию',
        related_name='titles',
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр произведения',
        help_text='Выберите жанр',
        related_name='titles',
    )
    objects = models.Manager()

    class Meta:
        """Метаданные."""
        verbose_name_plural = 'Произведения'
        verbose_name = 'Произведение'

    def __str__(self):
        return str(self.name)[:HEADER_LENGTH]


class Review(models.Model):
    """
     Отзывы, к произведениям.
     Пользователь может оставить только один отзыв на произведение.
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Название произведения',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(SCORE_MIN),
            MaxValueValidator(SCORE_MAX)
        ],
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
    )

    class Meta:
        default_related_name = 'reviews'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='такой отзыв уже существует'
            ),
        )

    def __str__(self):
        return self.text[:HEADER_LENGTH]


class Comment(models.Model):
    """
    Комментарии к отзывам.
    Пользователь может оставить много комментариев на отзыв.
    """
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
    )

    class Meta:
        default_related_name = 'comments'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:HEADER_LENGTH]
