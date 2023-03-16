from django.shortcuts import get_object_or_404

from rest_framework import filters, mixins, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


from reviews.models import Categories, Genres, Titles

from .permissions import IsAccountAdminOrReadOnly
from .serializers import (
    CategoriesSerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
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

    def create(self, request, *args, **kwargs):
        """
        Создание категории.
        """
        user = request.user.is_staff
        data = {
            "name": request.POST.get('name', None),
            "slug": request.POST.get('slug', None),
        }
        serializer = self.serializer_class(data=data,
                                           context={'author': user})
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Удаление категории.
        """
        instance = get_object_or_404(Categories, slug=self.kwargs.get('slug'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    def create(self, request, *args, **kwargs):
        """
        Создание жанра.
        """
        user = request.user.is_staff
        data = {
            "name": request.POST.get('name', None),
            "slug": request.POST.get('slug', None),
        }
        serializer = self.serializer_class(data=data,
                                           context={'author': user})
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Удаление жанра.
        """
        instance = get_object_or_404(Genres, slug=self.kwargs.get('slug'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Titles.
    """
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAccountAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category__slug', 'genre__slug', 'name', 'year',)

    def create(self, request, *args, **kwargs):
        """
        Создание жанра.
        """
        user = request.user.is_staff
        data = {
            "name": request.POST.get('name', None),
            "year": request.POST.get('year', None),
            "description": request.POST.get('description', None),
            "genre": request.POST.get('genre', None),
            "category": request.POST.get('category', None),
        }
        serializer = self.serializer_class(data=data,
                                           context={'author': user})
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        Частичное обновление информации о произведении.
        """
        user = request.user.is_staff
        instance = get_object_or_404(Titles, pk=self.kwargs.get('titles_id'))
        data = {
            "name": request.POST.get('name', None),
            "year": request.POST.get('year', None),
            "description": request.POST.get('description', None),
            "genre": request.POST.get('genre', None),
            "category": request.POST.get('category', None),
        }
        serializer = self.serializer_class(instance=instance,
                                           data=data,
                                           context={'author': user},
                                           partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Удаление произведения.
        """
        instance = get_object_or_404(Titles, pk=self.kwargs.get('titles_id'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Review.
    """
    serializer_class = ReviewSerializer

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
