from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator

from api_yamdb.settings import REGEX

from .models import User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField(read_only=True)
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())
                    ], required=True,)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())
                    ],
    )

    class Meta:
        model = User
        fields = ('__all__')


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if not REGEX.match(value) or value.lower() == 'me':
            raise serializers.ValidationError('Invalid username!')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=150, required=True)

    def validate_username(self, value):
        if not REGEX.match(value) or value.lower() == 'me':
            raise serializers.ValidationError('Invalid username!')
        if not User.objects.filter(username=value).exists():
            raise exceptions.NotFound('User not found!')
        return value


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
