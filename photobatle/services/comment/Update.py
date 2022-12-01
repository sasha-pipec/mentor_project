from django import forms
from django.core.exceptions import ObjectDoesNotExist
from service_objects.services import ServiceWithResult
from photobatle.models import *
from api.status_code import *


class UpdateCommentService(ServiceWithResult):
    """Service class for update comment"""

    comment = forms.CharField(required=False)
    id = forms.IntegerField(required=False)
    user_id = forms.IntegerField(required=False)

    custom_validations = ["validate_user_id", "validate_id", "validate_comment", "check_comment_author"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._update_comment
        return self

    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"Missing one of all requirements parameters: api token")

    def validate_id(self):
        try:
            return Comment.objects.get(pk=self.cleaned_data['id'])
        except ObjectDoesNotExist:
            if not self.cleaned_data['id']:
                raise ValidationError400(f"Missing one of all requirements parameters: id")
            raise ValidationError404(f"Incorrect id value")

    def validate_comment(self):
        if not self.cleaned_data['comment']:
            raise ValidationError400(f"Missing one of all requirements parameters: comment")

    def check_comment_author(self):
        try:
            return Comment.objects.get(pk=self.cleaned_data['id'],
                                       user_id=self.cleaned_data['user_id'])
        except ObjectDoesNotExist:
            raise ValidationError409(f"You are not the author of the comment")

    @property
    def _update_comment(self):
        comment = Comment.objects.get(pk=self.cleaned_data['id'])
        comment.content = self.cleaned_data['comment']
        comment.save()
        self.cleaned_data['slug'] = (Photo.objects.get(pk=comment.photo_id)).slug
        return comment
