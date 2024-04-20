from django.conf import settings
from django.core.mail import send_mail
from django.template import loader

NULLABLE = {'blank': True, 'null': True}


def send_welcome_message(user, password):
    html_message = loader.render_to_string(
        'message_welcome.html', context={
            'welcome': 'Добро пожаловать!',
            'introductory': 'Мы рады, что Вы с нами',
            'one_line': f'Ваш пароль {password}, '
                        f'для завершения авторизации необходимо получить токен на сайте по своему паролю. ',
            'two_line': f'По паролю Вы всегда можете обновить токен-авторизации на сайте.',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'note': 'Если вы не регистрировались на сайте, то проигнорируйте это письмо.'
        }
    )
    send_mail(
        subject='Поздравляем с регистрацией!',
        message=f'Ваш пароль {password}, '
                f'для завершения авторизации необходимо получить токен на сайте по своему паролю. '
                f'По паролю Вы всегда можете восстановить токен-авторизации на сайте.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
        html_message=html_message
    )

    # def send_welcome_message(email, password):
    #     send_mail(
    #         subject='Добро пожаловать!',
    #         message=f'Ваш пароль {password}, '
    #                 f'для завершения авторизации необходимо получить токен на сайте по своему паролю. '
    #                 f'По паролю Вы всегда можете восстановить токен-авторизации на сайте. '
    #                 f'Если вы не регистрировались на сайте, то проигнорируйте это письмо.',
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=[email],
    #         fail_silently=False,
    #     )

    # def send_new_password(email, new_password):
    #     send_mail(
    #         subject='Пароль изменён',
    #         message=f'Новый пароль {new_password}',
    #         from_email=settings.EMAIL_HOST_USER,
    #         recipient_list=[email],
    #         fail_silently=False,
    #     )
