from django import forms
from service_objects.services import Service
from photobatle.utils import *
from django.core.exceptions import ValidationError
from photobatle.models import *


class UpdatePhotoService(DataMixin, Service):
    """Service class for update photo"""

    def get_type_of_photo(self):
        if self.file and self.content_type.split('/')[1] != 'jpeg':
            raise ValidationError('Type of file is not jpeg, try again', code='invalid')

    slug = forms.SlugField()
    photo_name = forms.CharField(required=False)
    photo_content = forms.CharField(required=False)
    photo = forms.Field(required=False, validators=[get_type_of_photo])
    user_id = forms.IntegerField()

    def get_new_photo_name(self, value):
        self.cleaned_data['photo'].name = self.slug_russian_word(value)

    @property
    def validate_slug_id(self):
        try:
            return Photo.objects.get(slug=self.cleaned_data['slug'],
                                     user_id=self.cleaned_data['user_id'])
        except:
            raise ValidationError(f"Incorrect slug value", code='invalid')

    def process(self):
        if self.validate_slug_id:
            post = Photo.objects.get(slug=self.cleaned_data['slug'])

            if self.cleaned_data['photo'] and self.cleaned_data['photo'] != post.photo:
                self.get_new_photo_name(post.photo_name)
                post.previous_photo = post.photo
                post.photo = self.cleaned_data['photo']
            if self.cleaned_data['photo_name'] and self.cleaned_data['photo_name'] != post.photo_name:
                post.photo_name = self.cleaned_data['photo_name']
                post.slug = self.slug_russian_word(self.cleaned_data['photo_name'])
            if self.cleaned_data['photo_content'] and self.cleaned_data['photo_content'] != post.photo_content:
                post.photo_content = self.cleaned_data['photo_content']
            post.moderation = 'MOD'
            return post.save()
