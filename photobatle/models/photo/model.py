import os
import string
import random

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from django_counter_cache_field import CounterCacheField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from transliterate import translit

from photobatle.models.base_model.model import BaseModel


def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


class Photo(BaseModel):
    """Photo model"""

    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='User',
                             related_name='user_name_username')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    photo = models.ImageField(max_length=300, upload_to='photobatl/photos/',
                              blank=False, verbose_name='File')
    photo_imagekit_large = ImageSpecField(source='photo',
                                          processors=[ResizeToFill(450, 450)],
                                          format='JPEG',
                                          options={'quality': 60})
    photo_imagekit_medium = ImageSpecField(source='photo',
                                           processors=[ResizeToFill(350, 350)],
                                           format='JPEG',
                                           options={'quality': 60})
    previous_photo = models.ImageField(blank=True, verbose_name='Previous file')
    photo_name = models.CharField(max_length=255, blank=False, verbose_name='Title')
    photo_content = models.TextField(blank=False, verbose_name='Description')
    published_at = models.DateField(null=True, verbose_name='Date of publish')
    task_id = models.TextField(null=True, blank=True)
    comment_count = CounterCacheField()
    like_count = CounterCacheField()

    ON_DELETION = 'DELETION'
    ON_MODERATION = 'MODERATION'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'

    STATUS_CHOICES = (
        (ON_DELETION, 'On deletion'),
        (ON_MODERATION, 'On moderation'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    )
    moderation = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Status', default=ON_MODERATION)

    @receiver(pre_save)
    def set_slug(sender, instance, *args, **kwargs):
        if isinstance(instance, Photo):
            instance.photo.name = translit(instance.photo.name, 'ru', reversed=True)
            if not instance.slug:
                instance.slug = slugify(rand_slug() + "-" + translit(instance.photo_name, 'ru', reversed=True))

    def __str__(self):
        return self.photo_name

    def checking_the_existence(self):
        return os.path.exists(str(self.photo.url)[1::])

    def get_absolute_url(self):
        return reverse('detail_post', kwargs={'slug': self.slug})

    class Meta:
        app_label = 'photobatle'
        verbose_name_plural = 'Photo'
