from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserAdminListAPIView, UserCreateAPIView, UserRetrieveUpdateDestroyAPIView, \
    UserAdminRetrieveUpdateDestroyAPIView, UserResetPasswordAPIView

app_name = UsersConfig.name

urlpatterns = [
    # user
    path('user/create/', UserCreateAPIView.as_view(), name='user_create'),
    path('user/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user_user_RUD'),
    path('user/reset_password/', UserResetPasswordAPIView.as_view(), name='reset_password'),

    # user for Admin
    path('service/', UserAdminListAPIView.as_view(), name='user_list'),
    path('service/user/<int:pk>/', UserAdminRetrieveUpdateDestroyAPIView.as_view(), name='user_admin_RUD'),

    # tokens
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
