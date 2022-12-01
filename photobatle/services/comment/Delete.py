from django import forms
from django.core.exceptions import ObjectDoesNotExist
from service_objects.services import ServiceWithResult
from photobatle.models import *
from api.status_code import *


class DeleteCommentService(ServiceWithResult):
    """Service class for delete comment"""

    id = forms.IntegerField(required=False)
    user_id = forms.IntegerField(required=False)

    custom_validations = ["validate_user_id", "validate_id", "check_comment_author", "check_comment_children"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._deleted_comment
        return self

    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"incorrect api token")

    def validate_id(self):
        try:
            return Comment.objects.get(pk=self.cleaned_data['id'])
        except ObjectDoesNotExist:
            if not self.cleaned_data['id']:
                raise ValidationError400(f"Missing one of all requirements parameters: id")
            raise ValidationError404(f"Incorrect id value")

    def check_comment_author(self):
        try:
            return Comment.objects.get(pk=self.cleaned_data['id'],
                                       user_id=self.cleaned_data['user_id'])
        except ObjectDoesNotExist:
            raise ValidationError404(f"You are not the author of the comment")

    def check_comment_children(self):
        if Comment.objects.filter(parent_id=self.cleaned_data['id']):
            raise ValidationError409(f"Comment have children")

    @property
    def _deleted_comment(self):
        comment = Comment.objects.get(pk=self.cleaned_data['id'])
        comment.delete()
        return Photo.objects.get(pk=comment.photo_id)
