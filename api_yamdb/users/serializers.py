from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator

from .models import User, username_not_correct


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = ('email', 'username')
        model = User

    def validate_username(self, value):
        if username_not_correct(value):
            raise serializers.ValidationError('Invalid username!')
        return value


class AdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')

    def validate_username(self, value):
        if username_not_correct(value):
            raise serializers.ValidationError('Invalid username!')
        return value

    def validate_role(self, value):
        if (self.data['method'] == 'PATCH'
                and value != self.request.user.role):
            raise serializers.ValidationError('Invalid method role!')
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
