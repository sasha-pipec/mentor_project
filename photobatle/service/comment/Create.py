from django import forms
from service_objects.services import Service
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Count
from photobatle.models import *


class CreateCommentService(Service):
    """Service class for create comment"""

    comment = forms.CharField(required=False)
    parent_comment_id = forms.Field(required=False)
    photo_slug = forms.SlugField()
    user_id = forms.IntegerField()

    @property
    def validate_parent_comment_id(self):
        if not Comment.objects.filter(
                photo_id=(Photo.objects.get(slug=self.cleaned_data['photo_slug'])).id,
                pk=self.cleaned_data['parent_comment_id']):
            raise Exception(f"Incorrect parent_comment_id value")
        return True

    @property
    def validate_photo_slug(self):
        if not Photo.objects.filter(slug=self.cleaned_data['photo_slug']):
            raise Exception(f"Incorrect photo_slug value")
        return True

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

    def process(self):
        if self.validate_photo_slug:
            photo = Photo.objects.get(slug=self.cleaned_data['photo_slug'])
            if self.cleaned_data['comment']:
                if self.cleaned_data['parent_comment_id'] is None or self.cleaned_data['parent_comment_id'] == 'None':
                    # Creating a comment entry in the database
                    Comment.objects.create(
                        photo=Photo(pk=photo.id),
                        user_id=self.cleaned_data['user_id'],
                        content=self.cleaned_data['comment'])
                else:
                    # Creating a record of a response to a comment in the database
                    if self.validate_parent_comment_id:
                        Comment.objects.create(
                            photo=Photo(pk=photo.id),
                            user_id=self.cleaned_data['user_id'],
                            parent_id=self.cleaned_data['parent_comment_id'],
                            content=self.cleaned_data['comment'])
                self.send_notification()
