from django.contrib.auth.models import AbstractUser
from django.db import models

from config.сonstants import NULLABLE


class UserRoles(models.TextChoices):
    CONSUMER = 'consumer'
    ADMIN = 'admin'


class User(AbstractUser):
    """Модель пользователя, авторизация по email"""
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')

    phone = models.CharField(max_length=35, **NULLABLE, verbose_name='Телефон')
    image = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='Аватар')

    role = models.CharField(max_length=15, choices=UserRoles.choices, default=UserRoles.CONSUMER, verbose_name='Роль')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

