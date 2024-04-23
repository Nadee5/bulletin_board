from rest_framework import serializers

from board.models import Advert, Review


class ReviewSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели отзыва"""

    class Meta:
        model = Review
        fields = '__all__'


class AdvertSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели объявления"""
    review = ReviewSerializer(source='advert', many=True)

    class Meta:
        model = Advert
        fields = '__all__'
