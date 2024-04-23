from django.conf import settings
from django.core.mail import send_mail
from django.template import loader


def send_message_new_review(user, new_review):
    html_message = loader.render_to_string(
        'message.html', context={
            'welcome': 'Привет',
            'introductory': 'Рады видеть Вас',
            'one_line': f'На Ваше объявление оставлен отзыв: "{new_review}".',
            'two_line': f'Перейдите на сайт, чтобы увидеть детали.',
            'first_name': user.first_name,
            'last_name': user.last_name,
            'note': 'Если вы не регистрировались на сайте, то проигнорируйте это письмо.'
        }
    )
    send_mail(
        subject='Уведомление об отзыве по Вашему объявлению',
        message=f'На Ваше объявление оставлен отзыв! '
                f'Текст: "{new_review}". '
                f'Перейдите на сайт, чтобы увидеть детали.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
        html_message=html_message
    )
