from django.conf import settings
from django.db import models


class Advert(models.Model):
    """Модель объявления"""
    title = models.CharField(max_length=150, verbose_name='Название')
    price = models.IntegerField(verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               verbose_name='Автор', related_name='author_advert')

    def __str__(self):
        return f'{self.title} - {self.price} руб.'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ('-created_at',)


class Review(models.Model):
    """Модель отзыва"""
    text = models.TextField(verbose_name='Текст отзыва')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')

    advert = models.ForeignKey(Advert, on_delete=models.CASCADE, verbose_name='Объявление', related_name='advert')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                               verbose_name='Автор', related_name='author_review')

    def __str__(self):
        return f'{self.author}: {self.text}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-created_at',)
