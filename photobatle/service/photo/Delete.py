from django import forms
from django.db.models import Count

from photobatle import models
from service_objects.services import Service
from photobatle import tasks
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


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
            tasks.delete_photo.s(slug=self.cleaned_data['slug_id']).apply_async(countdown=20, task_id=photo.slug)
            photo.save()
