from django import forms

from photobatle import models
from service_objects.services import Service
from photobatle import tasks
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from photobatle.celery import app


class DeletePhotoService(Service):
    """Service class for delete photo"""

    slug_id = forms.SlugField()
    user_id = forms.IntegerField()

    @property
    def validate_slug_id(self):
        try:
            return models.Photomodels.Photo.objects.get(slug=self.cleaned_data['slug_id'],
                                                        user_id=self.cleaned_data['user_id'])
        except:
            raise Exception(f"Incorrect slug_id value")

    def send_notification(self):
        channel_layer = get_channel_layer()
        photo = models.Photomodels.Photo.objects.get(slug=self.cleaned_data['slug_id'])
        list_user_id = models.Commentmodels.Comment.objects.values('user_id').filter(
            photo_id=photo.pk).distinct()
        for user_id in list_user_id:
            username = models.Usermodels.User.objects.get(pk=user_id['user_id'])
            async_to_sync(channel_layer.group_send)(
                str(username), {
                    'type': 'message',
                    'message': f"Фото '{photo.photo_name}' отправленно на удаление."
                               f"Ваши комментарии скоро будут удалены."
                }
            )

    def process(self):
        if self.validate_slug_id:
            self.send_notification()
            photo = models.Photomodels.Photo.objects.get(slug=self.cleaned_data['slug_id'])
            photo.moderation = 'DEL'
            task = tasks.delete_photo.s(photo.slug).apply_async(countdown=20)
            photo.task_id = task.id
            photo.save()
