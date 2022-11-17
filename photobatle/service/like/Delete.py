from django import forms
from service_objects.services import ServiceWithResult
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Count
from photobatle.models import *
from api.status_code import *


class DeleteLikeService(ServiceWithResult):
    """Service class for delete like"""

    slug = forms.SlugField(required=False)
    user_id = forms.IntegerField(required=False)

    custom_validations = ["validate_user_id", "validate_slug"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._delete_like
            self.response_status = status.HTTP_204_NO_CONTENT
        return self

    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"incorrect api token")

    def validate_slug(self):
        try:
            return Photo.objects.get(slug=self.cleaned_data['slug'])
        except Exception:
            if not self.cleaned_data['slug']:
                raise ValidationError400(f'Missing one of all requirements parameters: slug')
            raise ValidationError404(f"Incorrect value of slug")

    @property
    def _delete_like(self):
        photo = Photo.objects.get(slug=self.cleaned_data['slug'])
        like = Like.objects.get(photo_id=photo.id, user_id=self.cleaned_data['user_id'])
        like.delete()
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
                'message': f"Пользователь {username} "
                           f"снял голос с фото '{photo.photo_name}'. "
                           f"Всего голосов:{photo.like_count}"
            }
        )
