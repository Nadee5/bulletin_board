from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.services import generate_new_password
from users.mail_funcs import send_welcome_message, send_new_password
from users.models import User
from users.permissions import IsOwner, IsAdmin
from users.serializers import UserSerializer, UserConsumerSerializer


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
        send_welcome_message(user, password)
        user.is_active = True
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer  # прописать get_serializer_class
    queryset = User.objects.all()
    permission_classes = [IsOwner | IsAdmin]


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwner | IsAdmin]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsOwner | IsAdmin]


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # permission_classes = [IsAdmin] # for test


class UserResetPasswordAPIView(APIView):
    """Восстановление доступа к аккаунту"""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if email:
            try:
                User.objects.get(email=email)
            except ObjectDoesNotExist:
                return Response({'error': 'Пользователь с такой почтой не зарегистрирован.'},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            raise ValueError('Введите почту для восстановления пароля.')

        user = User.objects.get(email=email)
        new_password = generate_new_password()
        user.set_password(new_password)
        send_new_password(user, new_password)
        user.save()
        return Response({'success': 'Пароль изменён и отправлен на почту.'}, status=status.HTTP_200_OK)
