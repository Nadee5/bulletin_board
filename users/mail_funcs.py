from django.conf import settings
from django.core.mail import send_mail
from django.template import loader


def send_welcome_message(user, password):
    html_message = loader.render_to_string(
        'message.html', context={
            'welcome': 'Добро пожаловать!',
            'introductory': 'Мы рады, что Вы с нами',
            'one_line': f'Ваш пароль {password}, '
                        'для завершения авторизации необходимо получить токен на сайте по своему паролю. ',
            'two_line': 'По паролю Вы всегда можете обновить токен-авторизации на сайте.',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'note': 'Если вы не регистрировались на сайте, то проигнорируйте это письмо.'
        }
    )
    send_mail(
        subject='Поздравляем с регистрацией!',
        message=f'Ваш пароль {password}, '
                'для завершения авторизации необходимо получить токен на сайте по своему паролю. '
                'По паролю Вы всегда можете восстановить токен-авторизации на сайте.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
        html_message=html_message
    )


def send_new_password(user, password):
    html_message = loader.render_to_string(
        'message.html', context={
            'welcome': 'Привет!',
            'introductory': 'Вы обновили пароль от своего аккаунта',
            'one_line': f'Ваш новый временный пароль {password}. ',
            'two_line': 'Рекомендуем авторизоваться на сайте и установить новый пароль.',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'note': 'Если вы не регистрировались на сайте, то проигнорируйте это письмо.'
        }
    )
    send_mail(
        subject='Восстановление пароля',
        message=f'Ваш пароль {password}. '
                f'По паролю Вы всегда можете восстановить токен-авторизации на сайте.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
        html_message=html_message
    )
