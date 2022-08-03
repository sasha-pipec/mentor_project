from django import forms
from service_objects.services import Service
from photobatle import models


class DeleteCommentService(Service):
    """Service class for delete comment"""

    comment_pk = forms.IntegerField()

    def process(self):

        comment = models.Commentmodels.Comment.objects.get(pk=self.cleaned_data['comment_pk'])
        comment.delete()

        return models.Photomodels.Photo.objects.get(pk=comment.photo_id)
