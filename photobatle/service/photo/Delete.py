from django import forms
from api.status_code import *
from service_objects.services import Service
from photobatle import tasks
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from photobatle.models import *


class DeletePhotoService(Service):
    """Service class for delete photo"""

    slug = forms.SlugField()
    user_id = forms.IntegerField(required=False)

    def process(self):
        self.validate_user_id
        self.validate_slug_id
        self.send_notification()
        photo = Photo.objects.get(slug=self.cleaned_data['slug'])
        photo.moderation = 'DEL'
        task = tasks.delete_photo.s(photo.slug).apply_async(countdown=20)
        photo.task_id = task.id
        photo.save()

    @property
    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"incorrect api token")

    @property
    def validate_slug_id(self):
        try:
            return Photo.objects.get(slug=self.cleaned_data['slug'],
                                     user_id=self.cleaned_data['user_id'])
        except:
            raise ValidationError400(f"Incorrect slug value")

    def send_notification(self):
        channel_layer = get_channel_layer()
        photo = Photo.objects.get(slug=self.cleaned_data['slug'])
        list_user_id = Comment.objects.values('user_id').filter(
            photo_id=photo.pk).distinct()
        for user_id in list_user_id:
            username = User.objects.get(pk=user_id['user_id'])
            async_to_sync(channel_layer.group_send)(
                str(username), {
                    'type': 'message',
                    'message': f"Фото '{photo.photo_name}' отправленно на удаление."
                               f"Ваши комментарии скоро будут удалены."
                }
            )