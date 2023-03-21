from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from api_yamdb.settings import MAX_LENGTH_EMAIL, MAX_LENGTH_USERNAME
from .models import MAX_LENGTH_ROLES, User
from .validators import validate_username


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Serializer для модели User.
    """
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all()),
                    validate_username
                    ], max_length=MAX_LENGTH_USERNAME, required=True,)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())
                    ], max_length=MAX_LENGTH_EMAIL, required=True,)

    class Meta:
        """
        Метаданные.
        """
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')


class UserSerializer(AdminUserSerializer):
    """
    Serializer для модели User.
    """
    role = serializers.CharField(max_length=MAX_LENGTH_ROLES, read_only=True)


class RegisterSerializer(AdminUserSerializer):
    """
    Serializer для регистрации.
    """
    class Meta:
        """
        Метаданные.
        """
        model = User
        fields = ('username', 'email',)


class TokenSerializer(AdminUserSerializer):
    """
    Serializer для токена.
    """
    confirmation_code = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME, required=True)

    class Meta:
        """
        Метаданные.
        """
        model = User
        fields = ('username', 'confirmation_code',)
