from functools import lru_cache

from django import forms
from service_objects.services import ServiceWithResult
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Count
from photobatle.models import User, Photo, Like


class DeleteLikeService(ServiceWithResult):
    """Service class for delete like"""

    slug = forms.SlugField(required=False)
    user_id = forms.IntegerField(required=False)

    def process(self):
        self.result = self._delete_like
        return self

    @property
    def _delete_like(self):
        photo = Photo.objects.get(slug=self.cleaned_data['slug'])
        like = Like.objects.get(photo_id=photo.id, user_id=self.cleaned_data['user_id'])
        like.delete()
        self.send_notification()
        return self._photo

    @property
    @lru_cache
    def _photo(self):
        return Photo.objects.annotate(like_count=Count('like_photo')).get(slug=self.cleaned_data['slug'])

    def send_notification(self):
        channel_layer = get_channel_layer()
        username = User.objects.get(pk=self.cleaned_data['user_id']).username
        async_to_sync(channel_layer.group_send)(
            str(self._photo.user), {
                'type': 'message',
                'message': f"User '{username}' "
                           f"delete like for photo '{self._photo.photo_name}'. "
                           f"All likes:{self._photo.like_count}"
            }
        )
