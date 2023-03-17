from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter

from reviews.models import Titles


class TitleFilter(FilterSet):
    """
    Фильтрация полей Titles.
    """
    name = CharFilter(field_name='name', lookup_expr='icontains')
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')
    year = NumberFilter(field_name='year')

    class Meta:
        """
        Метаданные.
        """
        model = Titles
        fields = '__all__'
