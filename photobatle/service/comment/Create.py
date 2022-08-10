from django import forms
from service_objects.services import Service
from photobatle import models
from rest_framework.authtoken.models import Token


class CreateCommentService(Service):
    """Service class for create comment"""

    comment = forms.CharField(required=False)
    parent_comment_id = forms.Field(required=False)
    photo_slug = forms.SlugField()
    user_id = forms.IntegerField(required=False)
    user_api_token = forms.CharField(required=False)

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

    @property
    def get_user_id(self):
        if self.cleaned_data['user_id']:
            return self.cleaned_data['user_id']
        try:
            return (Token.objects.get(key=self.cleaned_data['user_api_token'])).user_id
        except BaseException:
            raise Exception(f"Incorrect user_api_token value")

    def process(self):
        user = self.get_user_id
        if self.validate_photo_slug:
            photo = models.Photomodels.Photo.objects.get(slug=self.cleaned_data['photo_slug'])
            if self.cleaned_data['comment']:
                if self.cleaned_data['parent_comment_id'] is None or self.cleaned_data['parent_comment_id'] == 'None':
                    # Creating a comment entry in the database

                    models.Commentmodels.Comment.objects.create(
                        photo=models.Photomodels.Photo(pk=photo.id),
                        user_id=user,
                        content=self.cleaned_data['comment'])
                else:
                    # Creating a record of a response to a comment in the database
                    if self.validate_parent_comment_id:
                        models.Commentmodels.Comment.objects.create(
                            photo=models.Photomodels.Photo(pk=photo.id),
                            user_id=user,
                            parent_id=self.cleaned_data['parent_comment_id'],
                            content=self.cleaned_data['comment'])
