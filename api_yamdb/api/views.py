from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, viewsets

from reviews.models import Category, Genre, Review, Title
from .filter import TitleFilter
from .mixins import CustomMixinsViewSet
from .permissions import (IsAccountAdminOrReadOnly,
                          IsAuthorOrAdministratorOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer)


class CategoryViewSet(CustomMixinsViewSet):
    """ViewSet для модели Categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenresViewSet(CustomMixinsViewSet):
    """ViewSet для модели Genres."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Titles."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    permission_classes = (IsAccountAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    ordering = ('name', )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """POST для всех авторизованных, PATCH для модеров, админов и автора."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdministratorOrReadOnly,)

    @property
    def _title(self):
        return get_object_or_404(Title, id=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self._title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(title=self._title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdministratorOrReadOnly,)

    @property
    def _review(self):
        return get_object_or_404(Review, id=self.kwargs.get("review_id"))

    def get_queryset(self):
        return self._review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self._review)
