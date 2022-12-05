from functools import lru_cache

from django import forms
from django.db.models import Count
from service_objects.services import ServiceWithResult
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from photobatle.models import User, Photo, Like


class CreateLikeService(ServiceWithResult):
    """Service class for create like"""

    slug = forms.SlugField(required=False)
    user_id = forms.IntegerField(required=False)

    def process(self):
        self.result = self._create_like
        return self

    @property
    def _create_like(self):
        photo = Photo.objects.get(slug=self.cleaned_data['slug'])
        like = Like(photo_id=photo.id, user_id=self.cleaned_data['user_id'])
        like.save()
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
                'message': f"Your photo '{self._photo.photo_name}' "
                           f"liked user '{username}'. "
                           f"All likes:{self._photo.like_count}"
            }
        )
