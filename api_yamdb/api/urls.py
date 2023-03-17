from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CategoriesViewSet, GenresViewSet, TitleViewSet

api_router_v1 = DefaultRouter()

app_name = 'api'

api_router_v1.register(r'categories', CategoriesViewSet, basename='categories')
api_router_v1.register(r'genres', GenresViewSet, basename='genres')
api_router_v1.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(api_router_v1.urls)),
]
