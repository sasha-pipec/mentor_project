from django import forms
from service_objects.services import Service
from photobatle import models


class UpdateCommentService(Service):
    """Service class for update comment"""

    comment = forms.CharField()
    comment_pk = forms.IntegerField()

    def process(self):

        user_comment = models.Commentmodels.Comment.objects.get(pk=self.cleaned_data['comment_pk'])
        user_comment.content = self.cleaned_data['comment']
        user_comment.save()
        return models.Photomodels.Photo.objects.get(pk=user_comment.photo_id)
