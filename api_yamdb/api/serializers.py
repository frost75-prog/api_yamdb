from rest_framework import serializers

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
    )
    slug = serializers.SlugField(
        max_length=50,
        required=True,
        read_only=True,
    )

    class Meta:
        """Метаданные."""
        model = Categories
        fields = '__all__'

    def validate_slug(self, value):
        """Кастомный валидатор для поля slug."""
        if not REGEX_SLUG.match(value) or value.lower() == 'slug':
            raise serializers.ValidationError('Invalid slug!')
        return value


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализер для модели Genres.
    """
    name = serializers.CharField(
        max_length=256,
        required=True,
    )
    slug = serializers.SlugField(
        max_length=50,
        required=True,
        read_only=True,
    )

    class Meta:
        """Метаданные."""
        model = Genres
        fields = '__all__'

    def validate_slug(self, value):
        """Кастомный валидатор для поля slug."""
        if not REGEX_SLUG.match(value) or value.lower() == 'slug':
            raise serializers.ValidationError('Invalid slug!')
        return value


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализер для модели Titles.
    """
    name = serializers.CharField(
        max_length=256,
        required=True,
    )
    year = serializers.IntegerField(
        required=True,
    )
    genre = serializers.SlugRelatedField(
        many=True,
        required=True,
        slug_field='genre_title'
    )
    category = serializers.SlugField(
        required=True,
    )

    class Meta:
        """Метаданные."""
        model = Titles
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели Review.
    """
    author = serializers.SlugRelatedField(
        slug_field='username',
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
    )

    class Meta:
        """Метаданные."""
        model = Comment
        fields = '__all__'
        read_only_fields = (
            'author',
            'pub_date',
        )
