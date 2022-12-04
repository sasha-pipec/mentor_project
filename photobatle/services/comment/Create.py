from functools import lru_cache

from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Count
from photobatle.models import Comment, Photo, User


class CreateCommentService(ServiceWithResult):
    """Service class for create comment"""

    comment = forms.CharField()
    parent_comment_id = forms.IntegerField(required=False)
    slug = forms.SlugField()
    user = ModelField(User)

    def process(self):
        self.result = self._created_comment
        return self

    @property
    def _created_comment(self) -> Comment:
        self.send_notification()
        comment = Comment(
            photo=Photo(pk=(self._get_photo).id),
            user_id=self.cleaned_data['user'].id,
            parent_id=self.cleaned_data['parent_comment_id'],
            content=self.cleaned_data['comment']
        )
        comment.save()
        return comment

    @property
    @lru_cache()
    def _get_photo(self) -> Photo:
        return Photo.objects.annotate(comment_count=Count('comment_photo')).get(slug=self.cleaned_data['slug'])

    def send_notification(self):
        channel_layer = get_channel_layer()
        photo = self._get_photo
        username = self.cleaned_data['user'].username
        async_to_sync(channel_layer.group_send)(
            str(photo.user), {
                'type': 'message',
                'message': f"User {username} "
                           f"commented your photo '{photo.photo_name}'. "
                           f"Comment count:{photo.comment_count}"
            }
        )
