from django import forms
from service_objects.services import Service
from photobatle import models


class DeleteCommentService(Service):
    """Service class for delete comment"""

    comment_pk = forms.IntegerField()
    user_id = forms.IntegerField()

    @property
    def validate_comment_pk(self):
        try:
            models.Commentmodels.Comment.objects.get(pk=self.cleaned_data['comment_pk'],
                                                     user_id=self.cleaned_data['user_id'])
            if models.Commentmodels.Comment.objects.filter(parent_id=self.cleaned_data['comment_pk']):
                raise Exception(f"Comment have children")
            return True
        except:
            raise Exception(f"Incorrect comment_pk value")

    def process(self):
        if self.validate_comment_pk:
            comment = models.Commentmodels.Comment.objects.get(pk=self.cleaned_data['comment_pk'])
            comment.delete()
            return models.Photomodels.Photo.objects.get(pk=comment.photo_id)
