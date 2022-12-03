from functools import lru_cache

from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from photobatle import tasks
from photobatle.models import Photo, User, Comment


class DeletePhotoService(ServiceWithResult):
    """Service class for delete photo"""

    slug = forms.SlugField()
    user = ModelField(User)

    def process(self):
        self.result = self._delete_photo
        return self

    @property
    def _delete_photo(self):
        self.send_notification()
        photo = self._get_photo
        photo.moderation = Photo.ON_DELETION
        task = tasks.delete_photo.s(photo.slug).apply_async(countdown=20)
        photo.task_id = task.id
        photo.save()

    @property
    @lru_cache()
    def _get_photo(self):
        return Photo.objects.get(slug=self.cleaned_data['slug'])

    def send_notification(self):
        channel_layer = get_channel_layer()
        photo = self._get_photo
        username_list = []
        query_objects = Comment.objects.filter(photo_id=photo.pk).select_related('user')
        for obj in query_objects:
            username_list.append(str(obj.user.username))
        for user in set(username_list):
            async_to_sync(channel_layer.group_send)(
                str(user), {
                    'type': 'message',
                    'message': f"Photo '{photo.photo_name}' send on deletion."
                               f"Your comments will be deleted."
                }
            )
