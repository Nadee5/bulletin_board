from rest_framework import serializers

from board.models import Advert, Review


class AdvertSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели объявления"""

    class Meta:
        model = Advert
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели отзыва"""

    class Meta:
        model = Review
        fields = '__all__'
