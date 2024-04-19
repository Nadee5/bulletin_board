from django.conf import settings
from django.core.mail import send_mail

NULLABLE = {'blank': True, 'null': True}


def send_welcome_message(email, password):
    send_mail(
        subject='Добро пожаловать!',
        message=f'Ваш пароль {password}, '
                f'для завершения авторизации необходимо получить токен на сайте по своему паролю. '
                f'По паролю Вы всегда можете восстановить токен-авторизации на сайте. '
                f'Если вы не регистрировались на сайте, то проигнорируйте это письмо.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )


# def send_new_password(email, new_password):
#     send_mail(
#         subject='Пароль изменён',
#         message=f'Новый пароль {new_password}',
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[email],
#         fail_silently=False,
#     )
