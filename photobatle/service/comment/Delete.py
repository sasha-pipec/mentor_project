from django import forms
from service_objects.services import Service
from photobatle.models import *


class DeleteCommentService(Service):
    """Service class for delete comment"""

    comment_id = forms.IntegerField()
    user_id = forms.IntegerField()

    @property
    def validate_comment_pk(self):
        try:
            if Comment.objects.filter(parent_id=self.cleaned_data['comment_id']):
                raise Exception(f"Comment have children")
            return Comment.objects.get(pk=self.cleaned_data['comment_id'],
                                       user_id=self.cleaned_data['user_id'])
        except:
            raise Exception(f"Incorrect comment_id value")

    def process(self):
        if self.validate_comment_pk:
            comment = Comment.objects.get(pk=self.cleaned_data['comment_id'])
            comment.delete()
            return Photo.objects.get(pk=comment.photo_id)
