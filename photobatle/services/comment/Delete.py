from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from photobatle.models import Comment, Photo, User


class DeleteCommentService(ServiceWithResult):
    """Service class for delete comment"""

    id = forms.IntegerField(required=False)
    user = ModelField(User)

    def process(self):
        self.result = self._deleted_comment
        return self

    @property
    def _deleted_comment(self):
        comment = Comment.objects.get(pk=self.cleaned_data['id'])
        comment.delete()
        return Photo.objects.get(pk=comment.photo_id)
