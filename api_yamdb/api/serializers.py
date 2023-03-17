from datetime import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Categories, Genres, Titles, Review, Comment,\
    SCORE_MIN, SCORE_MAX

from api_yamdb.settings import REGEX_SLUG


class CategoriesSerializer(serializers.ModelSerializer):
    """"
    Сериализер для модели Categories.
    """
    name = serializers.CharField(
        max_length=256,
        required=True,
        validators=[UniqueValidator(queryset=Categories.objects.all())]
    )
    slug = serializers.SlugField(
        max_length=50,
        required=True,
        validators=[UniqueValidator(queryset=Categories.objects.all())]
    )
    lookup_field = 'slug'

    class Meta:
        """Метаданные."""
        model = Categories
        fields = '__all__'

    def validate_name(self, value):
        """Кастомный валидатор для поля name."""
        if len(value) > 256:
            raise serializers.ValidationError('Invalid slug!')
        return value

    def validate_slug(self, value):
        """Кастомный валидатор для поля slug."""
        if not REGEX_SLUG.match(value):
            raise serializers.ValidationError('Invalid slug!')
        elif len(value) > 50:
            raise serializers.ValidationError('Invalid slug!')
        return value


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализер для модели Genres.
    """
    name = serializers.CharField(
        max_length=256,
        required=True,
        validators=[UniqueValidator(queryset=Genres.objects.all())]
    )
    slug = serializers.SlugField(
        max_length=50,
        required=True,
        validators=[UniqueValidator(queryset=Genres.objects.all())]
    )
    lookup_field = 'slug'

    class Meta:
        """Метаданные."""
        model = Genres
        fields = '__all__'

    def validate_name(self, value):
        """Кастомный валидатор для поля name."""
        if len(value) > 256:
            raise serializers.ValidationError('Invalid slug!')
        return value

    def validate_slug(self, value):
        """Кастомный валидатор для поля slug."""
        if not REGEX_SLUG.match(value):
            raise serializers.ValidationError('Invalid slug!')
        elif len(value) > 50:
            raise serializers.ValidationError('Invalid slug!')
        return value


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализер для модели Titles.
    """
    name = serializers.CharField(
        max_length=256,
        required=True,
        validators=[UniqueValidator(queryset=Titles.objects.all())]
    )
    year = serializers.IntegerField(
        required=True,
        validators=[UniqueValidator(queryset=Titles.objects.all())]
    )
    category = CategoriesSerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )

    class Meta:
        """Метаданные."""
        model = Titles
        fields = '__all__'

    def validate_name(self, value):
        """Кастомный валидатор для поля name."""
        if len(value) > 256:
            raise serializers.ValidationError('Invalid slug!')
        return value

    def validate_year(self, value):
        """
        Кастомный валидатор для поля year.
        Год выпуска не может быть больше текущего.
        """
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Invalid year! Year must be less then current year.')
        elif value < 0:
            raise serializers.ValidationError(
                'Invalid year! Year must be biggest then zero.')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели Review.
    """
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    text = serializers.CharField(
        required=True,
    )

    class Meta:
        """Метаданные."""
        model = Review
        fields = '__all__'
        read_only_fields = (
            'author',
            'pub_date',
        )

    def validate_score(self, value):
        """Кастомный валидатор для поля score."""
        if value not in range(SCORE_MIN, SCORE_MAX):
            raise serializers.ValidationError(
                'Значение вне допутимого диапазона!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели Comment.
    """
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        """Метаданные."""
        model = Comment
        fields = '__all__'
        read_only_fields = (
            'pub_date',
        )
