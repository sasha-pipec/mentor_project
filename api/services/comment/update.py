from functools import lru_cache

from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from photobatle.models import Comment, User


class ApiUpdateCommentService(ServiceWithResult):
    """Service class for update comment"""

    comment = forms.CharField(required=False)
    id = forms.IntegerField(required=False)
    user = ModelField(User, required=False)

    def process(self):
        self.check_required_parameters_presence()
        if self.is_valid():
            self.check_comment_presence_by_id()
            if self.is_valid():
                self.result = self._update_comment
        return self

    @property
    def _update_comment(self) -> Comment:
        comment = self.check_comment_presence_by_id()
        comment.content = self.cleaned_data['comment']
        comment.save()
        return comment

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
