from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    '''Переопределенная модель user'''
    photo = models.FileField(upload_to='user/photos/%Y/%m/%d', verbose_name='Фото', max_length=255)


class Photo(models.Model):
    '''Модель фотографий'''
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='+')
    photo = models.ImageField(upload_to='photobatl', verbose_name='Фото')
    photo_name = models.CharField(max_length=255, verbose_name='Имя фото')
    photo_content = models.TextField(blank=False, verbose_name='Описание фото')
    date_published_on_site = models.DateField(auto_now=True, verbose_name='Дата публикации')
    like_count = models.IntegerField(default=0, verbose_name='Лайки')
    comment_count = models.IntegerField(default=0, verbose_name='Комментарии')
    moderation = models.BooleanField(null=False, verbose_name='Одобрено модератором')

    class Meta:
        verbose_name_plural = 'Фото'
