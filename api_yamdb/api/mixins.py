from rest_framework import filters, mixins, viewsets

from .permissions import IsAccountAdminOrReadOnly


class ModelMixinCreateReadDelete(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Кастомный набор контройлеров.
    (CRD - create, read, delete)
    """
    permission_classes = (IsAccountAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
