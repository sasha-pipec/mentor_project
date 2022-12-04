from functools import lru_cache

from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from photobatle.models import Photo, User, Comment


class ApiDeleteCommentService(ServiceWithResult):
    """Service class for delete comment"""

    id = forms.IntegerField(required=False)
    user = ModelField(User, required=False)

    custom_validations = ["check_comment_presence_by_id", "check_comment_children"]

    def process(self):
        self.check_required_parameters_presence()
        if self.is_valid():
            self.run_custom_validations()
            if self.is_valid():
                self.result = self._deleted_comment
        return self

    @property
    def _deleted_comment(self):
        comment = self.check_comment_presence_by_id()
        comment.delete()
        return Photo.objects.get(pk=comment.photo_id)

    def check_required_parameters_presence(self):
        for field in self.fields:
            if not self.cleaned_data[str(field)]:
                field = field if str(field) != 'user' else 'api token'
                self.errors[str(field)] = f"Missing one of all requirements parameters:{str(field)}"

    @lru_cache
    def check_comment_presence_by_id(self):
        comment = Comment.objects.filter(pk=self.cleaned_data['id'], user_id=self.cleaned_data['user'].id)
        if comment:
            return comment.first()
        self.errors['comment_not_found'] = f"Comment with id '{self.cleaned_data['id']}' not found," \
                                           " mb its not your comment"

    def check_comment_children(self):
        if Comment.objects.filter(parent_id=self.cleaned_data['id']):
            self.errors['conflict'] = "Comment have children"
