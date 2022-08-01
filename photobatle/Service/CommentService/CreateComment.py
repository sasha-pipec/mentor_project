from django import forms
from service_objects.services import Service
from photobatle import models


class CreateCommentService(Service):
    """Service class for create comment"""

    comment = forms.CharField(required=False)
    parent_comment_id = forms.Field()
    pk = forms.IntegerField()
    user_id = forms.IntegerField()

    def process(self):
        comment = self.cleaned_data['comment']
        parent_comment_id = self.cleaned_data['parent_comment_id']
        pk = self.cleaned_data['pk']
        user_id = self.cleaned_data['user_id']

        if comment:
            if parent_comment_id == 'none':
                # Creating a comment entry in the database
                models.Commentmodels.Comment.objects.create(photo=models.Photomodels.Photo(pk=pk),
                                                            user_id=user_id, content=comment)
            else:
                # Creating a record of a response to a comment in the database
                models.Commentmodels.Comment.objects.create(photo=models.Photomodels.Photo(pk=pk),
                                                            user_id=user_id,
                                                            parent_id=parent_comment_id,
                                                            content=comment)

        return (models.Photomodels.Photo.objects.get(pk=pk)).slug
