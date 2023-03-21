from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api_yamdb.settings import API_VERSION_SLUG
from .views import (
    CategoryViewSet, CommentViewSet,
    GenresViewSet, TitleViewSet,
    ReviewViewSet)
from users.views import UserViewSet, register, token

api_router = DefaultRouter()

app_name = 'api'

api_router.register('categories', CategoryViewSet, basename='categories')
api_router.register('genres', GenresViewSet, basename='genres')
api_router.register('titles', TitleViewSet, basename='titles')
api_router.register('users', UserViewSet, basename='users')
api_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
api_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path(API_VERSION_SLUG, include(api_router.urls)),
    path(f'{API_VERSION_SLUG}auth/signup/', register, name='register'),
    path(f'{API_VERSION_SLUG}auth/token/', token, name='login'),
]
