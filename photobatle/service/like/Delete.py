from django import forms
from service_objects.services import Service
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Count
from photobatle.models import *


class DeleteLikeService(Service):
    """Service class for delete like"""

    photo_id = forms.IntegerField()
    user_id = forms.IntegerField()

    @property
    def validate_photo_id(self):
        try:
            return Photo.objects.get(pk=self.cleaned_data['photo_id'])
        except Exception:
            raise Exception(f"Incorrect photo_id value")

    @property
    def get_like(self):
        try:
            return Like.objects.get(photo_id=self.cleaned_data['photo_id'],
                                    user_id=self.cleaned_data['user_id'])
        except Exception:
            raise Exception(f"Photo dont have like from this user")

    def send_notification(self):
        channel_layer = get_channel_layer()
        photo = Photo.objects.annotate(like_count=Count('like_photo')).get(
            pk=self.cleaned_data['photo_id'])
        username = str(User.objects.get(pk=self.cleaned_data['user_id']))
        async_to_sync(channel_layer.group_send)(
            str(photo.user), {
                'type': 'message',
                'message': f"Пользователь {username} "
                           f"снял голос с фото '{photo.photo_name}'. "
                           f"Всего голосов:{photo.like_count}"
            }
        )

    def process(self):
        if self.validate_photo_id:
            if self.get_like:
                like = Like.objects.get(photo_id=self.cleaned_data['photo_id'],
                                        user_id=self.cleaned_data['user_id'])
                like.delete()
                self.send_notification()
                return (Photo.objects.get(pk=self.cleaned_data['photo_id'])).slug
