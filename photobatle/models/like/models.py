from django.db import models


class Like(models.Model):
    """Like model"""
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE, verbose_name='Фото',
                              related_name='like_photo')

    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь',
                                  related_name='user_name_like')

    class Meta:
        app_label = 'photobatle'
        verbose_name_plural = 'Лайки'
