from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class User(AbstractUser):
    """User model"""
    photo = models.FileField(upload_to='user/photos/%Y/%m/%d', verbose_name='Photo', max_length=255)
    photo_imagekit_medium = ImageSpecField(source='photo',
                                           processors=[ResizeToFill(350, 350)],
                                           format='JPEG',
                                           options={'quality': 60})

    def __str__(self):
        return self.username

    class Meta:
        app_label = 'photobatle'
        verbose_name_plural = 'User'
