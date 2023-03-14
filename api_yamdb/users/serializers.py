import re

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        regex = re.compile(r'^[\w.@+-]+\z')
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                'A user with this username already exists.')
        if not regex.match(value) or value.lower() == 'me':
            raise serializers.ValidationError('Invalid username.')
        return value

    class Meta:
        model = User
        fields = '__all__'
