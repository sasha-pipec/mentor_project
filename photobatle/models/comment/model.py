from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django_counter_cache_field import connect_counter

from photobatle.models.base_model.model import BaseModel


class Comment(BaseModel):
    """Comment model"""
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE, verbose_name='Photo',
                              related_name='comment_photo')
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='User',
                             related_name='user_name_photo')
    content = models.TextField(verbose_name='Comment content', max_length=300)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE,
                               verbose_name='Parent of comment',
                               related_name='parent_comment')

    @receiver(pre_save)
    def update_photo_comment_count(sender, instance, *args, **kwargs):
        connect_counter('comment_count', Comment.photo)

    def __str__(self):
        return self.content

    class Meta:
        app_label = 'photobatle'
        verbose_name_plural = 'Comment'
