from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser

from board.models import Advert, Review
from board.serializers import AdvertSerializer, ReviewSerializer
from users.permissions import IsOwner, IsAdmin


class AdvertListAPIView(generics.ListAPIView):
    """Просмотра списка объявлений"""
    serializer_class = AdvertSerializer
    queryset = Advert.objects.all()
    permission_classes = [AllowAny]


class UserAdvertListAPIView(generics.ListAPIView):
    """Просмотра списка объявлений текущего пользователя"""
    serializer_class = AdvertSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        """Фильтрация списка объявлений по текущему пользователю"""
        return Advert.objects.filter(author=self.request.user)


class AdvertCreateAPIView(generics.CreateAPIView):
    """Cоздание объявления"""
    serializer_class = AdvertSerializer

    def perform_create(self, serializer):
        """Привязка текущего пользователя к создаваемому объекту"""
        new_advert = serializer.save()
        new_advert.author = self.request.user
        new_advert.save()


class AdvertRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр объявления"""
    serializer_class = AdvertSerializer
    queryset = Advert.objects.all()


class AdvertUpdateAPIView(generics.UpdateAPIView):
    """Редактирование объявления"""
    serializer_class = AdvertSerializer
    queryset = Advert.objects.all()
    permission_classes = [IsOwner | IsAdmin]


class AdvertDestroyAPIView(generics.DestroyAPIView):
    """Удаление объявления"""
    queryset = Advert.objects.all()
    permission_classes = [IsOwner | IsAdmin]


class ReviewListAPIView(generics.ListAPIView):
    """Просмотр списка отзывов"""
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """Фильтрация списка отзывов по объявлениям текущего пользователя"""
        return Review.objects.filter(author=self.request.user)  # оставленные мной

        # попытка 100500
        # author_advert = Advert.objects.filter(author=self.request.user)
        # return Review.objects.filter(advert=author_advert)

        # return Review.objects.filter(author_advert=self.request.user)


class ReviewCreateAPIView(generics.CreateAPIView):
    """Cоздание отзыва"""
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        """Привязка текущего пользователя к создаваемому объекту"""
        new_review = serializer.save()
        new_review.author = self.request.user
        new_review.save()


class ReviewUpdateAPIView(generics.UpdateAPIView):
    """Редактирование отзыва"""
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsOwner | IsAdmin]


class ReviewDestroyAPIView(generics.DestroyAPIView):
    """Удаление отзыва"""
    queryset = Review.objects.all()
    permission_classes = [IsOwner | IsAdmin]
