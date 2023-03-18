from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    """
    Фильтрация полей Titles.
    """
    name = CharFilter(field_name='name', lookup_expr='icontains')
    category = CharFilter(field_name='category__slug', lookup_expr='icontains')
    genre = CharFilter(field_name='genre__slug', lookup_expr='icontains')
    year = NumberFilter(field_name='year', lookup_expr='icontains')

    class Meta:
        """
        Метаданные.
        """
        model = Title
        fields = '__all__'
