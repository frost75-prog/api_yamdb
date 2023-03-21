from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title, Review, Comment, SCORE_MAX, \
    SCORE_MIN
from api_yamdb.settings import MAX_NAME_LENGTH, MAX_SLUG_NAME


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer для модели Category.
    """
    name = serializers.CharField(
        max_length=MAX_NAME_LENGTH,
        required=True,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )
    slug = serializers.SlugField(
        max_length=MAX_SLUG_NAME,
        required=True,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        """Метаданные."""
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(CategorySerializer):
    """
    Serializer для модели Genre.
    """
    name = serializers.CharField(
        max_length=MAX_NAME_LENGTH,
        required=True,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )
    slug = serializers.SlugField(
        max_length=MAX_SLUG_NAME,
        required=True,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        """Метаданные."""
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    """
    Serializer для модели Title.
    """
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        """Метаданные."""
        fields = (
            'id', 'category', 'genre', 'year', 'name', 'description', 'rating')
        model = Title
        read_only_fields = (
            'id', 'year', 'name', 'description',)


class TitleWriteSerializer(serializers.ModelSerializer):
    """
    Serializer для модели Title.
    """
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        """Метаданные."""
        fields = ('id', 'category', 'genre', 'year', 'name', 'description')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели Review.
    """

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    score = serializers.IntegerField(
        max_value=SCORE_MAX,
        min_value=SCORE_MIN,
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Вы не можете добавить более одного отзыва на произведение'
                )
        return data

    class Meta:
        """Метаданные."""
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


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
        fields = ('id', 'text', 'author', 'pub_date')
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
