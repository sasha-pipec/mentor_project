from django import forms
from service_objects.services import Service
from photobatle.models import *
from api.status_code import *


class DeleteCommentService(Service):
    """Service class for delete comment"""

    comment_id = forms.IntegerField()
    user_id = forms.IntegerField(required=False)

    def process(self):
        self.validate_user_id
        if self.validate_comment_pk:
            comment = Comment.objects.get(pk=self.cleaned_data['comment_id'])
            comment.delete()
            return Photo.objects.get(pk=comment.photo_id)
        raise ValidationError409(f"Comment have children")

    @property
    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"incorrect api token")

    @property
    def validate_comment_pk(self):
        try:
            if Comment.objects.filter(parent_id=self.cleaned_data['comment_id']):
                return False
            return Comment.objects.get(pk=self.cleaned_data['comment_id'],
                                       user_id=self.cleaned_data['user_id'])
        except:
            raise ValidationError400(f"Incorrect comment_id value")
