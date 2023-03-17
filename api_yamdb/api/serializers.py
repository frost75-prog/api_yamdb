from datetime import datetime

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator

from reviews.models import Categories, Genres, Titles, Review, Comment, \
    SCORE_MIN, SCORE_MAX, CHOICES

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
        validators=[UniqueValidator(queryset=Categories.objects.all())]
    )

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
    )
    slug = serializers.SlugField(
        max_length=50,
        required=True,
        validators=[UniqueValidator(queryset=Genres.objects.all())]
    )

    class Meta:
        """Метаданные."""
        model = Genres
        fields = '__all__'

    def validate_name(self, value):
        """Кастомный валидатор для поля name."""
        if len(value) >= 256:
            raise serializers.ValidationError('Invalid slug!')
        return value

    def validate_slug(self, value):
        """Кастомный валидатор для поля slug."""
        if not REGEX_SLUG.match(value):
            raise serializers.ValidationError('Invalid slug!')
        elif len(value) >= 50:
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
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True,
    )
    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug',
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
    score = serializers.ChoiceField(
        choices=CHOICES,
    )

    class Meta:
        """Метаданные."""
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = (
            'author',
            'pub_date',
            'title',
        )

    def validate_score(self, value):
        """Кастомный валидатор для поля score."""
        value = int(value)
        if value not in range(SCORE_MIN, SCORE_MAX):
            raise serializers.ValidationError(
                'Значение вне допутимого диапазона!')
        print(value)
        return value

    def validate(self, data):
        """
        Валидатор на один юзер-один отзыв на произведение.
        """
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        author = self.context['request'].user
        if self.context['request'].method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Вы не можете оставить второй отзыв на произведение.'
                )
        return data

    def create(self, validated_data):
        review = Review.objects.create(
            title=get_object_or_404(
                Titles,
                pk=self.context.get('view').kwargs.get('title_id')
            ),
            text=validated_data.get('text'),
            author=self.context['request'].user,
            score=validated_data.get('score'),
        )
        return review


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели Comment.
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
        model = Comment
        fields = '__all__'
        read_only_fields = (
            'author',
            'pub_date',
            'review',
        )

    def create(self, validated_data):
        comment = Comment.objects.create(
            review=get_object_or_404(
                Review,
                pk=self.context.get('view').kwargs.get('review_id')
            ),
            text=validated_data.get('text'),
            author=self.context['request'].user,
        )
        return comment
