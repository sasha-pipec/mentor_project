from django import forms
from django.core.exceptions import ObjectDoesNotExist
from service_objects.services import ServiceWithResult
from photobatle.models import *
from api.status_code import *


class DeleteCommentService(ServiceWithResult):
    """Service class for delete comment"""

    comment_id = forms.IntegerField()
    user_id = forms.IntegerField(required=False)

    custom_validations = ["validate_user_id", "validate_comment_id", "check_comment_author", "check_comment_children"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._deleted_comment
        return self

    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"incorrect api token")

    def validate_comment_id(self):
        try:
            return Comment.objects.get(pk=self.cleaned_data['comment_id'])
        except ObjectDoesNotExist:
            raise ValidationError404(f"Incorrect comment_id value")

    def check_comment_author(self):
        try:
            return Comment.objects.get(pk=self.cleaned_data['comment_id'],
                                       user_id=self.cleaned_data['user_id'])
        except ObjectDoesNotExist:
            raise ValidationError404(f"You are not the author of the comment")

    def check_comment_children(self):
        if Comment.objects.filter(parent_id=self.cleaned_data['comment_id']):
            raise ValidationError409(f"Comment have children")

    @property
    def _deleted_comment(self):
        comment = Comment.objects.get(pk=self.cleaned_data['comment_id'])
        comment.delete()
        return Photo.objects.get(pk=comment.photo_id)
