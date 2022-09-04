from django.db import models


class Comment(models.Model):
    """Comment model"""
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE, verbose_name='Фото',
                              related_name='comment_photo')
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь',
                                  related_name='user_name_photo')
    content = models.TextField(verbose_name='Текст комментария', max_length=300)
    parent = models.ForeignKey('self', blank=True,null=True, on_delete=models.CASCADE, verbose_name='Родитель комментария',
                               related_name='parent_comment')
    create_at = models.DateField(null=True, auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.content

    class Meta:
        app_label = 'photobatle'
        verbose_name_plural = 'Комментарии'
