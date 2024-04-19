from django.urls import path

from board.apps import BoardConfig
from board.views import AdvertListAPIView, UserAdvertListAPIView, AdvertCreateAPIView, AdvertRetrieveAPIView, \
    AdvertUpdateAPIView, AdvertDestroyAPIView, ReviewListAPIView, ReviewCreateAPIView, ReviewUpdateAPIView, \
    ReviewDestroyAPIView

app_name = BoardConfig.name

urlpatterns = [
    # Advert
    path('', AdvertListAPIView.as_view(), name='advert_list'),
    path('my_ads/', UserAdvertListAPIView.as_view(), name='my_advert_list'),
    path('create/', AdvertCreateAPIView.as_view(), name='advert_create'),
    path('view/<int:pk>/', AdvertRetrieveAPIView.as_view(), name='advert_retrieve'),
    path('update/<int:pk>/', AdvertUpdateAPIView.as_view(), name='advert_update'),
    path('delete/<int:pk>/', AdvertDestroyAPIView.as_view(), name='advert_delete'),

    # Review
    path('review/', ReviewListAPIView.as_view(), name='review_list'),
    path('review/create/', ReviewCreateAPIView.as_view(), name='review_create'),
    path('review/update/<int:pk>/', ReviewUpdateAPIView.as_view(), name='review_update'),
    path('review/delete/<int:pk>/', ReviewDestroyAPIView.as_view(), name='review_delete'),
]
