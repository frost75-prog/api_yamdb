from django.urls import include, path

from rest_framework.routers import DefaultRouter

from users.views import register, token
from .views import CategoriesViewSet, GenresViewSet, TitleViewSet

api_router_v1 = DefaultRouter()

api_router_v1.register('categories', CategoriesViewSet, basename='categories')
api_router_v1.register('genres', GenresViewSet, basename='genres')
api_router_v1.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(api_router_v1.urls)),
    path('auth/signup/', register, name='register'),
    path('auth/token/', token, name='login'),
]
