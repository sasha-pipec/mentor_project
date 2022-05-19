from django.apps import AppConfig


class PhotobatleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'photobatle'
    verbose_name='Фотоконкурс'

    def ready(self):
        import photobatle.signals

