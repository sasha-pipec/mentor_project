from django import forms
from service_objects.services import Service
from photobatle import models
from rest_framework.authtoken.models import Token


class CreateCommentService(Service):
    """Service class for create comment"""

    comment = forms.CharField(required=False)
    parent_comment_id = forms.Field(required=False)
    photo_slug = forms.SlugField()
    user_id = forms.IntegerField()

    @property
    def validate_parent_comment_id(self):
        if not models.Commentmodels.Comment.objects.filter(
                photo_id=(models.Photomodels.Photo.objects.get(slug=self.cleaned_data['photo_slug'])).id,
                pk=self.cleaned_data['parent_comment_id']):
            raise Exception(f"Incorrect parent_comment_id value")
        return True

    @property
    def validate_photo_slug(self):
        if not models.Photomodels.Photo.objects.filter(slug=self.cleaned_data['photo_slug']):
            raise Exception(f"Incorrect photo_slug value")
        return True

    def process(self):
        if self.validate_photo_slug:
            photo = models.Photomodels.Photo.objects.get(slug=self.cleaned_data['photo_slug'])
            if self.cleaned_data['comment']:
                if self.cleaned_data['parent_comment_id'] is None or self.cleaned_data['parent_comment_id'] == 'None':
                    # Creating a comment entry in the database

                    models.Commentmodels.Comment.objects.create(
                        photo=models.Photomodels.Photo(pk=photo.id),
                        user_id=self.cleaned_data['user_id'],
                        content=self.cleaned_data['comment'])
                else:
                    # Creating a record of a response to a comment in the database
                    if self.validate_parent_comment_id:
                        models.Commentmodels.Comment.objects.create(
                            photo=models.Photomodels.Photo(pk=photo.id),
                            user_id=self.cleaned_data['user_id'],
                            parent_id=self.cleaned_data['parent_comment_id'],
                            content=self.cleaned_data['comment'])
