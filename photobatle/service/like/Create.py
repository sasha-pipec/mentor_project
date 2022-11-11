from django import forms
from django.db.models import Count
from service_objects.services import ServiceWithResult
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from photobatle.models import *
from api.status_code import *


class CreateLikeService(ServiceWithResult):
    """Service class for create like"""

    photo_id = forms.IntegerField()
    user_id = forms.IntegerField(required=False)

    custom_validations = ["validate_user_id", "validate_photo_id", "validate_author_of_photo", "check_like"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._create_like
        return self

    def validate_photo_id(self):
        try:
            Photo.objects.get(pk=self.cleaned_data['photo_id'])
        except Exception:
            raise ValidationError404(f"Incorrect photo_id value")

    def validate_author_of_photo(self):
        photo = Photo.objects.get(pk=self.cleaned_data['photo_id'])
        if photo.user.id == self.cleaned_data['user_id']:
            raise ValidationError409(f"You can't like this photo, because it is your photo")

    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"incorrect api token")

    def check_like(self):
        if Like.objects.filter(photo_id=self.cleaned_data['photo_id'],
                               user_id=self.cleaned_data['user_id']):
            raise ValidationError409(f"Photo can have one like from one user")

    @property
    def _create_like(self):
        Like.objects.create(photo_id=self.cleaned_data['photo_id'],
                            user_id=self.cleaned_data['user_id'])
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
                'message': f"Ваше фото '{photo.photo_name}' "
                           f"понравилось пользователю {username}. "
                           f"Всего голосов:{photo.like_count}"
            }
        )
