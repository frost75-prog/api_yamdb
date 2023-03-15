from django.contrib.auth.tokens import default_token_generator as tg
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import (DEFAULT_FROM_EMAIL, DEFAULT_SUBJECT_EMAIL,
                                DEFAULT_TEXT_EMAIL)
from .models import User
from .permissions import IsAdmin
from .serializers import ForAdminSerializer, ForUserSerializer, TokenSerializer


def send_confirmation_code(user):
    """Отправка кода на почту"""
    return send_mail(DEFAULT_SUBJECT_EMAIL,
                     DEFAULT_TEXT_EMAIL.format(tg.make_token(user)),
                     DEFAULT_FROM_EMAIL,
                     [user.email])


class UserViewSet(viewsets.ModelViewSet):
    """Работа со своими данными для пользователя"""
    queryset = User.objects.all()
    serializer_class = ForAdminSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    pagination_class = PageNumberPagination

    @action(
        detail=False, methods=['get', 'patch'],
        url_path='me', url_name='me',
        permission_classes=(IsAuthenticated,)
    )
    def users_profile(self, request):
        """Профайл пользователя"""
        serializer = ForUserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = ForUserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Отправка и создание кода"""
    serializer = ForUserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    send_confirmation_code(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    """Получаем токен"""
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, username=serializer.data['username'])
    if not tg.check_token(user, serializer.data['confirmation_code']):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    token = AccessToken.for_user(user)
    return Response(
        {'token': str(token)}, status=status.HTTP_200_OK)
