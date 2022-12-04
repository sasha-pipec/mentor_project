from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from photobatle.models import Photo, Comment, User


class UpdateCommentService(ServiceWithResult):
    """Service class for update comment"""

    comment = forms.CharField()
    id = forms.IntegerField()
    user = ModelField(User)

    def process(self):
        self.result = self._update_comment
        return self

    @property
    def _update_comment(self) -> Comment:
        comment = Comment.objects.get(pk=self.cleaned_data['id'])
        comment.content = self.cleaned_data['comment']
        comment.save()
        self.cleaned_data['slug'] = (Photo.objects.get(pk=comment.photo_id)).slug
        return comment
