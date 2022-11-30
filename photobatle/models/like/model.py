from django.db import models


class Like(models.Model):
    """Like model"""
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE, verbose_name='Photo',
                              related_name='like_photo')

    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='User',
                             related_name='user_name_like')

    class Meta:
        app_label = 'photobatle'
        verbose_name_plural = 'Like'
        unique_together = ['photo', 'user']
