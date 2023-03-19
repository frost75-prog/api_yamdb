from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator

from .models import User, username_not_correct


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Serializer для модели User.
    """
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())
                    ], max_length=150, required=True,)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())
                    ], max_length=254, required=True,)

    class Meta:
        """
        Метаданные.
        """
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, value):
        """
        Валидация username.
        Корректность полей.
        """
        if username_not_correct(value):
            raise serializers.ValidationError('Invalid username!')
        return value


class UserSerializer(AdminUserSerializer):
    """
    Serializer для модели User.
    Дочерний класс.
    """
    role = serializers.CharField(max_length=9, read_only=True)


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


class TokenSerializer(serializers.Serializer):
    """
    Serializer для токена.
    """
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=150, required=True)

    def validate_username(self, value):
        """
        Валидация username.
        Корректность полей.
        """
        if username_not_correct(value):
            raise serializers.ValidationError('Invalid username!')
        if not User.objects.filter(username=value).exists():
            raise exceptions.NotFound('User not found!')
        return value
