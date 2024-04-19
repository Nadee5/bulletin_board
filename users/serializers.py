from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели пользователя"""

    class Meta:
        model = User
        fields = '__all__'


class UserConsumerSerializer(serializers.ModelSerializer):
    """Пользовательский сериализатор для модели пользователя"""

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'image',)
