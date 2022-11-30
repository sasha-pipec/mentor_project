from django.db import models


class BaseModel(models.Model):
    create_at = models.DateField(null=True, auto_now_add=True, verbose_name='Date of create')
    updated_at = models.DateField(auto_now=True, verbose_name='Date of update')

    class Meta:
        abstract = True
        app_label = 'photobatle'
        verbose_name_plural = 'Base model'
