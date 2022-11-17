from functools import lru_cache

from django import forms
from api.status_code import *
from service_objects.services import ServiceWithResult
from photobatle import tasks
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from photobatle.models import *


class DeletePhotoService(ServiceWithResult):
    """Service class for delete photo"""

    slug = forms.SlugField(required=False)
    user_id = forms.IntegerField(required=False)

    custom_validations = ["validate_user_id", "validate_slug", ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._delete_photo
        return self

    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"incorrect api token")

    def validate_slug(self):
        try:
            return Photo.objects.get(slug=self.cleaned_data['slug'], user_id=self.cleaned_data['user_id'])
        except Exception:
            if not self.cleaned_data['slug']:
                raise ValidationError400(f'Missing one of all requirements parameters: slug')
            raise ValidationError404(f"Incorrect slug value")

    @property
    @lru_cache()
    def _get_photo(self):
        return Photo.objects.get(slug=self.cleaned_data['slug'])

    @property
    def _delete_photo(self):
        self.send_notification()
        photo = self._get_photo
        photo.moderation = 'DEL'
        task = tasks.delete_photo.s(photo.slug).apply_async(countdown=20)
        photo.task_id = task.id
        photo.save()
        return task.id

    def send_notification(self):
        channel_layer = get_channel_layer()
        photo = self._get_photo
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
