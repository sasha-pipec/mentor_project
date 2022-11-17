from django import forms
from django.db.models import Count
from service_objects.services import ServiceWithResult
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from photobatle.models import *
from api.status_code import *


class CreateLikeService(ServiceWithResult):
    """Service class for create like"""

    slug = forms.SlugField(required=False)
    user_id = forms.IntegerField(required=False)

    custom_validations = ["validate_user_id", "validate_slug", "validate_author_of_photo"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._create_like
            self.response_status = status.HTTP_201_CREATED
        return self

    def validate_slug(self):
        try:
            Photo.objects.get(slug=self.cleaned_data['slug'])
        except Exception:
            if not self.cleaned_data['slug']:
                raise ValidationError400(f'Missing one of all requirements parameters: slug')
            raise ValidationError404(f"Incorrect value of slug")

    def validate_author_of_photo(self):
        photo = Photo.objects.get(slug=self.cleaned_data['slug'])
        if photo.user.id == self.cleaned_data['user_id']:
            raise ValidationError409(f"You can't like this photo, because it is your photo")

    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"incorrect api token")

    @property
    def _create_like(self):
        photo = Photo.objects.get(slug=self.cleaned_data['slug'])
        Like.objects.create(photo_id=photo.id,
                            user_id=self.cleaned_data['user_id'])
        self.send_notification()
        return Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                      like_count=Count('like_photo', distinct=True)).get(
            slug=self.cleaned_data['slug'])

    def send_notification(self):
        channel_layer = get_channel_layer()
        photo = Photo.objects.annotate(like_count=Count('like_photo')).get(
            slug=self.cleaned_data['slug'])
        username = str(User.objects.get(pk=self.cleaned_data['user_id']))
        async_to_sync(channel_layer.group_send)(
            str(photo.user), {
                'type': 'message',
                'message': f"Ваше фото '{photo.photo_name}' "
                           f"понравилось пользователю {username}. "
                           f"Всего голосов:{photo.like_count}"
            }
        )
