from rest_framework import serializers

from reviews.models import Categories, Genres, Titles

from api_yamdb.settings import REGEX_SLUG


class CategoriesSerializer(serializers.ModelSerializer):
    """
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
