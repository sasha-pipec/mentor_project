import os
from django.db import models
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Photo(models.Model):
    """Photo model"""

    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='user_name_username')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    photo = models.ImageField(max_length=300, upload_to='photobatl/photos/',
                              blank=False, verbose_name='Фото')
    photo_imagekit_large = ImageSpecField(source='photo',
                                          processors=[ResizeToFill(450, 450)],
                                          format='JPEG',
                                          options={'quality': 60})
    photo_imagekit_medium = ImageSpecField(source='photo',
                                           processors=[ResizeToFill(350, 350)],
                                           format='JPEG',
                                           options={'quality': 60})
    previous_photo = models.ImageField(blank=True, verbose_name='Предыдущее фото')
    photo_name = models.CharField(max_length=255, blank=False, unique=True, verbose_name='Имя фото')
    photo_content = models.TextField(blank=False, verbose_name='Описание фото')
    create_at = models.DateField(null=True, auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата обновления')
    published_at = models.DateField(null=True, verbose_name='Дата публикации')
    task_id = models.TextField(null=True, blank=True)

    ON_DELETION = 'DEL'
    ON_MODERATION = 'MOD'
    APPROVED = 'APR'
    REJECTED = 'REJ'

    STATUS_CHOICES = (
        (ON_DELETION, 'On deletion'),
        (ON_MODERATION, 'On moderation'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    )
    moderation = models.CharField(max_length=3, choices=STATUS_CHOICES, verbose_name='Статус', default=ON_MODERATION)

    def __str__(self):
        return self.photo_name

    def checking_the_existence(self):
        return os.path.exists(str(self.photo.url)[1::])

    def get_absolute_url(self):
        return reverse('detail_post', kwargs={'slug': self.slug})

    class Meta:
        app_label = 'photobatle'
        verbose_name_plural = 'Фото'
