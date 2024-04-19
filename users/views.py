from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from config.services import send_welcome_message
from users.models import User
from users.permissions import IsOwner, IsAdmin
from users.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Переопределение метода для сохранения хешированного пароля в бд
        (если пароль не хешируется - пользователь не считается активным
        и токен авторизации не создается).
        Отправка приветственного письма с паролем на почту."""
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        password = serializer.data["password"]
        user = User.objects.get(pk=serializer.data["id"])
        user.set_password(password)
        user.is_active = True
        user.save()
        send_welcome_message(email=user.email, password=password)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer #прописать get_serializer_class
    queryset = User.objects.all()
    permission_classes = [IsOwner | IsAdmin]


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwner]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsOwner | IsAdmin]


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]


# @login_required
# def get_new_password(request):
#     serializer = UserSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     password = serializer.data["password"]
#     user = User.objects.get(id=serializer.data["id"])
#     user.set_password(password)
#     user.is_active = True
#     user.save()
#     send_new_password(user.email, password)
#
#     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

