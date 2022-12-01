from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from transliterate import translit

from photobatle.utils import DataMixin
from photobatle.models import Photo, User
from api.status_code import *


class UpdatePhotoService(DataMixin, ServiceWithResult):
    """Service class for update photo"""

    slug = forms.SlugField(required=False)
    name = forms.CharField(required=False)
    content = forms.CharField(required=False)
    photo = forms.ImageField(required=False)
    user = ModelField(User)

    custom_validations = ["validate_user", "validate_slug", ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._update_photo
        return self

    @property
    def _update_photo(self):
        post = Photo.objects.get(slug=self.cleaned_data['slug'])

        if self.cleaned_data['photo'] and self.cleaned_data['photo'] != post.photo:
            self.validate_type_of_photo
            self.set_new_photo_name(post.photo_name)
            post.previous_photo = post.photo
            post.photo = self.cleaned_data['photo']
            post.moderation = Photo.ON_MODERATION
        if self.cleaned_data['name'] and self.cleaned_data['name'] != post.photo_name:
            self.validate_photo_name
            post.photo_name = self.cleaned_data['name']
            post.slug = self.slug_russian_word(self.cleaned_data['name'])
        if self.cleaned_data['content'] and self.cleaned_data['content'] != post.photo_content:
            post.photo_content = self.cleaned_data['content']
        post.save()
        return post

    def validate_user(self):
        if not self.cleaned_data['user']:
            raise ValidationError401(f"Missing one of all requirements parameters: api_token")

    def validate_slug(self):
        if not self.cleaned_data['slug']:
            raise ValidationError400(f"Missing one of all requirements parameters: slug")
        elif not Photo.objects.filter(slug=self.cleaned_data['slug'], user_id=self.cleaned_data['user'].id):
            raise ValidationError404(f"Incorrect slug value", code='invalid')

    def set_new_photo_name(self, value):
        self.cleaned_data['photo'].name = translit(self.cleaned_data['photo'].name, 'ru', reversed=True)

    @property
    def validate_type_of_photo(self):
        if self.cleaned_data['photo'].content_type.split('/')[1] != 'jpeg':
            raise ValidationError409(f"Incorrect type of photo,try jpeg", code='invalid')

    @property
    def validate_photo_name(self):
        if Photo.objects.filter(photo_name=self.cleaned_data['name']):
            raise ValidationError409(f"Photo with that name already exists", code='invalid')
        if Photo.objects.filter(slug=self.slug_russian_word(self.cleaned_data['name'])):
            raise ValidationError409(f"Photo with that slug already exists, try new photo name", code='invalid')
