from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser

from board.mail_funcs import send_message_new_review
from board.models import Advert, Review
from board.paginators import AdvertPaginator
from board.serializers import AdvertSerializer, ReviewSerializer
from users.permissions import IsOwner, IsAdmin


class AdvertListAPIView(generics.ListAPIView):
    """Просмотра списка объявлений"""
    serializer_class = AdvertSerializer
    queryset = Advert.objects.all()
    permission_classes = [AllowAny]

    pagination_class = AdvertPaginator

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ('author',)
    ordering_fields = ('title', '-created_at', 'price')
    search_fields = ('title',)


class UserAdvertListAPIView(generics.ListAPIView):
    """Просмотра списка объявлений текущего пользователя"""
    serializer_class = AdvertSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        """Фильтрация списка объявлений по текущему пользователю"""
        return Advert.objects.filter(author=self.request.user.id)


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
    """Список отзывов, оставленных текущем пользователем"""
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """Фильтрация списка объявлений"""
        return Review.objects.filter(author=self.request.user)


class UserReviewListAPIView(generics.ListAPIView):
    """Список отзывов, оставленных на объявления текущего пользователя"""
    serializer_class = ReviewSerializer

    def get_queryset(self):
        """Фильтрация списка объявлений"""
        return Review.objects.filter(advert__author=self.request.user.id)


class ReviewCreateAPIView(generics.CreateAPIView):
    """Cоздание отзыва"""
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        """Привязка текущего пользователя к создаваемому объекту"""
        new_review = serializer.save()
        new_review.author = self.request.user
        new_review.save()

        user = new_review.advert.author
        send_message_new_review(user, new_review)


class ReviewUpdateAPIView(generics.UpdateAPIView):
    """Редактирование отзыва"""
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsOwner | IsAdmin]


class ReviewDestroyAPIView(generics.DestroyAPIView):
    """Удаление отзыва"""
    queryset = Review.objects.all()
    permission_classes = [IsOwner | IsAdmin]
