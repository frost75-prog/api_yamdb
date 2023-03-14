import re

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.
    """

    def validate_username(self, value):
        """Валидация имени пользователя."""
        regex = re.compile(r'^[\w.@+-]+\z')
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                'A user with this username already exists.')
        if not regex.match(value) or value.lower() == 'me':
            raise serializers.ValidationError('Invalid username.')
        return value

    class Meta:
        """Методанные."""
        model = User
        fields = '__all__'
