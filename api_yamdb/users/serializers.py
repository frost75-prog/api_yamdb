from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator

from api_yamdb.settings import REGEX

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('role', )

    def validate_username(self, value):
        if not REGEX.match(value) or value.lower() == 'me':
            raise serializers.ValidationError('Invalid username!')
        return value


class AdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, value):
        if not REGEX.match(value) or value.lower() == 'me':
            raise serializers.ValidationError('Invalid username!')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=200, required=True)

    def validate_username(self, value):
        if not REGEX.match(value) or value.lower() == 'me':
            raise serializers.ValidationError('Invalid username!')
        if not User.objects.filter(username=value).exists():
            raise exceptions.NotFound('User not found!')
        return value
