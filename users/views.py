from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.services import generate_new_password
from users.mail_funcs import send_welcome_message, send_new_password
from users.models import User
from users.permissions import IsAdmin, IsSelf
from users.serializers import UserSerializer, UserAdminSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """Регистрация Пользователя."""
    serializer_class = UserAdminSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Переопределение метода для сохранения хешированного пароля в бд
        (если пароль не хешируется - пользователь не считается активным
        и токен авторизации не создается).
        Отправка приветственного письма с паролем на почту."""
        serializer = UserAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        password = serializer.data["password"]
        user = User.objects.get(pk=serializer.data["id"])
        user.set_password(password)
        send_welcome_message(user, password)
        user.is_active = True
        user.save()
        send_welcome_message(user, password)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserResetPasswordAPIView(APIView):
    """Восстановление доступа к аккаунту."""
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


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Точка входа для Пользователя: просмотр, редактирование, удаление СВОЕГО аккаунта."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsSelf]


class UserAdminRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Точка входа для Администратора: просмотр, редактирование, удаление аккаунта."""
    serializer_class = UserAdminSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]


class UserAdminListAPIView(generics.ListAPIView):
    """Точка входа для Администратора: просмотр списка аккаунтов."""
    serializer_class = UserAdminSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin] # for test
