from django import forms
from service_objects.services import Service
from photobatle.models import *


class UpdateCommentService(Service):
    """Service class for update comment"""

    comment = forms.CharField()
    comment_id = forms.IntegerField()
    user_id = forms.IntegerField()

    @property
    def validate_comment_pk(self):
        try:
            return Comment.objects.get(pk=self.cleaned_data['comment_id'],
                                       user_id=self.cleaned_data['user_id'])
        except:
            raise Exception(f"Incorrect comment_id value")

    def process(self):
        if self.validate_comment_pk:
            user_comment = Comment.objects.get(pk=self.cleaned_data['comment_id'])
            user_comment.content = self.cleaned_data['comment']
            user_comment.save()
            return Photo.objects.get(pk=user_comment.photo_id)
