from django.contrib.auth.tokens import \
    default_token_generator as token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import (DEFAULT_FROM_EMAIL, DEFAULT_SUBJECT_EMAIL,
                                DEFAULT_TEXT_EMAIL)
from .models import User
from .permissions import IsAdmin
from .serializers import (AdminUserSerializer, RegisterSerializer,
                          TokenSerializer, UserSerializer)


def send_confirmation_code(user):
    """Отправка кода на почту"""
    return send_mail(DEFAULT_SUBJECT_EMAIL,
                     DEFAULT_TEXT_EMAIL.format(
                         token_generator.make_token(user)),
                     DEFAULT_FROM_EMAIL,
                     [user.email])


class UserViewSet(viewsets.ModelViewSet):
    """Работа с данными для пользователя"""
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(IsAuthenticated,),
        serializer_class=UserSerializer
    )
    def users_profile(self, request):
        """Профайл пользователя"""
        serializer = self.get_serializer(request.user)
        if request.method == 'GET':
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Отправка и создание кода"""
    if User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')).exists():
        return Response(status=status.HTTP_200_OK)
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    send_confirmation_code(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    """Получаем токен"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=serializer.data['username'])
    if not token_generator.check_token(
            user, serializer.data['confirmation_code']):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    token = AccessToken.for_user(user)
    return Response(
        {'token': str(token)}, status=status.HTTP_200_OK)
