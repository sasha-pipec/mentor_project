from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    '''Переопределенная модель user'''
    photo = models.FileField(upload_to='user/photos/%Y/%m/%d', verbose_name='Фото', max_length=255)

    def __str__(self):
        return self.username

    class Meta:
        app_label = 'photobatle'
        verbose_name_plural = 'Пользователи'