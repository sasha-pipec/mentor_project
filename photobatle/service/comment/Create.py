from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from service_objects.services import ServiceWithResult
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Count
from photobatle.models import *
from api.status_code import *


class CreateCommentService(ServiceWithResult):
    """Service class for create comment"""

    comment = forms.CharField(required=False)
    parent_comment_id = forms.Field(required=False)
    photo_slug = forms.SlugField()
    user_id = forms.IntegerField(required=False)

    custom_validations = ["validate_user_id", "validate_photo_slug", "validate_parent_comment_id", ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._created_comment
        return self

    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"incorrect api token")

    def validate_parent_comment_id(self):
        if not self._parent_comment_id:
            raise ValidationError404(f"Incorrect parent_comment_id value")

    def validate_photo_slug(self):
        if not Photo.objects.filter(slug=self.cleaned_data['photo_slug']):
            raise ValidationError404(f"Incorrect photo_slug value")

    @property
    def _parent_comment_id(self):
        try:
            if self.cleaned_data["parent_comment_id"] and self.cleaned_data["parent_comment_id"] != "None":
                return Comment.objects.get(photo_id=(self._get_photo).id, pk=self.cleaned_data['parent_comment_id'])
            else:
                self.cleaned_data["parent_comment_id"] = None
                return True
        except ObjectDoesNotExist:
            return False

    @property
    def _created_comment(self):
        if self.cleaned_data['comment']:
            return Comment.objects.create(
                photo=Photo(pk=(self._get_photo).id),
                user_id=self.cleaned_data['user_id'],
                parent_id=self.cleaned_data['parent_comment_id'],
                content=self.cleaned_data['comment'])

    @property
    @lru_cache()
    def _get_photo(self):
        return Photo.objects.get(slug=self.cleaned_data['photo_slug'])

    def send_notification(self):
        channel_layer = get_channel_layer()
        photo = Photo.objects.annotate(comment_count=Count('comment_photo')).get(
            slug=self.cleaned_data['photo_slug'])
        username = str(User.objects.get(pk=self.cleaned_data['user_id']))
        async_to_sync(channel_layer.group_send)(
            str(photo.user), {
                'type': 'message',
                'message': f"Пользователь {username} "
                           f"оставил комментарий под фото '{photo.photo_name}'. "
                           f"Всего коментариев:{photo.comment_count}"
            }
        )
