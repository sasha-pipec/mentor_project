from django import forms
from service_objects.services import ServiceWithResult
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Count
from photobatle.models import *
from api.status_code import *


class DeleteLikeService(ServiceWithResult):
    """Service class for delete like"""

    photo_id = forms.IntegerField()
    user_id = forms.IntegerField(required=False)

    custom_validations = ["validate_user_id", "validate_photo_id", "check_like"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._delete_like
        return self

    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"incorrect api token")

    def validate_photo_id(self):
        try:
            return Photo.objects.get(pk=self.cleaned_data['photo_id'])
        except Exception:
            raise ValidationError404(f"Incorrect photo_id value")

    def check_like(self):
        try:
            return Like.objects.get(photo_id=self.cleaned_data['photo_id'],
                                    user_id=self.cleaned_data['user_id'])
        except Exception:
            raise ValidationError409(f"Photo dont have like from this user")

    @property
    def _delete_like(self):
        like = Like.objects.get(photo_id=self.cleaned_data['photo_id'], user_id=self.cleaned_data['user_id'])
        like.delete()
        self.send_notification()
        return Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                      like_count=Count('like_photo', distinct=True)).get(
            pk=self.cleaned_data['photo_id'])

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
