from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
# from rest_framework.permissions import

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from reviews.models import Categories, Genres, Titles, Review

from .permissions import IsAccountAdminOrReadOnly
from .filter import TitleFilter
from .serializers import (
    CategoriesSerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer, CommentSerializer,
)


class CategoriesViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """
    ViewSet для модели Categories.
    """
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
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
    queryset = Genres.objects.all()
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
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAccountAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Review.
    """
    serializer_class = ReviewSerializer
    permission_classes = (AllowAny,)

    @property
    def _title(self):
        return get_object_or_404(Titles, id=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self._title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=self._title
        )


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Comment.
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # def get_title(self):
    #     return get_object_or_404(Titles, id=self.kwargs.get("title_id"))

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
            post=self._review,
        )
