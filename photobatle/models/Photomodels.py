import datetime
import os

from django.db import models
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Photo(models.Model):
    '''Модель фотографий'''
    user_name = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь',
                                  related_name='user_name_username')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    photo = models.ImageField(max_length=300, upload_to='photobatl/photos/', verbose_name='Фото')
    photo_imagekit = ImageSpecField(source='photo',
                                    processors=[ResizeToFill(450, 450)],
                                    format='JPEG',
                                    options={'quality': 60})
    photo_name = models.CharField(max_length=255, verbose_name='Имя фото')
    photo_content = models.TextField(blank=False, verbose_name='Описание фото')
    date_published_on_site = models.DateField(auto_now=False, verbose_name='Дата публикации')

    STATUS_CHOICES = (
        ('1', 'На удалении'),
        ('2', 'На модерации'),
        ('3', 'Одобренно'),
    )
    moderation = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='Статус')

    def __str__(self):
        return self.photo_name

    def save(self, *args, **kwargs):
        if self.moderation == '3':
            self.date_published_on_site = datetime.datetime.now()
        super(Photo, self).save(*args, **kwargs)

    def checking_the_existence(self):
        if os.path.exists(str(self.photo.url)[1::]):
            return "exists"
        else:
            return "not exists"

    def get_absolute_url(self):
        return reverse('detail_post', kwargs={'slug_id': self.slug})

    class Meta:
        app_label = 'photobatle'
        verbose_name_plural = 'Фото'
