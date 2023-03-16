from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CategoriesViewSet, GenresViewSet, TitleViewSet,\
    ReviewViewSet

api_router_v1 = DefaultRouter()

app_name = 'api'

api_router_v1.register('categories', CategoriesViewSet, basename='categories')
api_router_v1.register('genres', GenresViewSet, basename='genres')
api_router_v1.register('titles', TitleViewSet, basename='titles')
api_router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
# api_router_v1.register('titles', TitleViewSet, basename='titles')


urlpatterns = [
    path('', include(api_router_v1.urls)),
]
