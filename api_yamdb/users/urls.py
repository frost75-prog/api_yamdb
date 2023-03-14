from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, register, token

app_name = 'users'

router_v1 = DefaultRouter()
router_v1.register('users/', UserViewSet, basename='users')

urlpatterns = [
    path('/', include(router_v1.urls)),
    path('auth/signup/', register, name='register'),
    path('auth/token/', token, name='login'),
]
