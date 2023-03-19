from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from reviews.models import Category, Genre, Review, Title

from .filter import TitleFilter
from .permissions import (IsAccountAdminOrReadOnly,
                          IsAuthorOrAdministratorOrReadOnly,
                          IsAuthorOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer)


class CategoryViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """
    ViewSet для модели Categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAccountAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """
    ViewSet для модели Genres.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAccountAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Titles.
    """
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all().order_by('name')
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return (AllowAny(),)
        return (IsAccountAdminOrReadOnly(),)

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
    """
    ViewSet для модели Comment.
    """
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    )

    @property
    def _review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get("review_id")
        )

    def get_queryset(self):
        return self._review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self._review,
        )
