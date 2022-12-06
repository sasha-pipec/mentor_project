from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_counter_cache_field import connect_counter


class Like(models.Model):
    """Like model"""
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE, verbose_name='Photo',
                              related_name='like_photo')

    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='User',
                             related_name='user_name_like')

    @receiver(pre_save)
    def update_photo_like_count(sender, instance, *args, **kwargs):
        connect_counter('like_count', Like.photo)

    class Meta:
        app_label = 'photobatle'
        verbose_name_plural = 'Like'
        unique_together = ['photo', 'user']
