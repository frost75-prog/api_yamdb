from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator

from .models import User, username_not_correct


class ForUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role', )

    def validate_username(self, value):
        if username_not_correct(value):
            raise serializers.ValidationError('Invalid username!')
        return value

    def validate_email(self, value):
        if len(value) > 254:
            raise serializers.ValidationError('Invalid email!')
        return value


class ForAdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, value):
        if username_not_correct(value):
            raise serializers.ValidationError('Invalid username!')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=150, required=True)

    def validate_username(self, value):
        if username_not_correct(value):
            raise serializers.ValidationError('Invalid username!')
        if not User.objects.filter(username=value).exists():
            raise exceptions.NotFound('User not found!')
        return value
