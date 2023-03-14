from django.db import models

from users.models import User


HEADER_LENGTH = 50


class Categories(models.Model):
    """
    Категории (типы) произведений («Фильмы», «Книги», «Музыка»).
    Одно произведение может быть привязано только к одной категории.
    """
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг-индентификатор',
    )

    class Meta:
        """Метаданные."""
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'
        ordering = ('id',)

    def __str__(self):
        return str(self.name)


class Genres(models.Model):
    """
    Жанры произведений.
    Одно произведение может быть привязано к нескольким жанрам.
    """
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг-индентификатор',
    )

    class Meta:
        """Метаданные."""
        verbose_name_plural = 'Жанры'
        verbose_name = 'Жанр'
        ordering = ('id',)

    def __str__(self):
        return str(self.name)


class Titles(models.Model):
    """
    Произведения, к которым пишут отзывы,
    (определённый фильм, книга или песенка).
    """
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    genre = models.ForeignKey(
        Genres,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Жанр произведения',
    )
    category = models.OneToOneField(
        Categories,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория произведения',
    )

    class Meta:
        """Метаданные."""
        verbose_name_plural = 'Произведения'
        verbose_name = 'Произведение'
        ordering = ('id',)

    def __str__(self):
        return str(self.name)


class Review(models.Model):
    """
     Отзывы, к произведениям.
     Пользователь может оставить только один отзыв на произведение.
    """
    title = models.OneToOneField(
        Titles,
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
    score = models.IntegerField(
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
    )

    class Meta:
        default_related_name = 'reviews'
        ordering = ('-pub_date',)

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
