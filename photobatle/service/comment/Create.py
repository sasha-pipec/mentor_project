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

        if self.cleaned_data['comment']:
            if self.cleaned_data['parent_comment_id'] == 'none':
                # Creating a comment entry in the database
                models.Commentmodels.Comment.objects.create(photo=models.Photomodels.Photo(pk=self.cleaned_data['pk']),
                                                            user_id=self.cleaned_data['user_id'],
                                                            content=self.cleaned_data['comment'])
            else:
                # Creating a record of a response to a comment in the database
                models.Commentmodels.Comment.objects.create(photo=models.Photomodels.Photo(pk=self.cleaned_data['pk']),
                                                            user_id=self.cleaned_data['user_id'],
                                                            parent_id=self.cleaned_data['parent_comment_id'],
                                                            content=self.cleaned_data['comment'])

        return (models.Photomodels.Photo.objects.get(pk=self.cleaned_data['pk'])).slug
