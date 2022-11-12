from django import forms
from service_objects.services import ServiceWithResult
from photobatle.utils import *
from photobatle.models import *
from api.status_code import *


class UpdatePhotoService(DataMixin, ServiceWithResult):
    """Service class for update photo"""

    slug = forms.SlugField()
    photo_name = forms.CharField(required=False)
    photo_content = forms.CharField(required=False)
    photo = forms.Field(required=False)
    user_id = forms.IntegerField(required=False)

    custom_validations = ["validate_user_id", "validate_slug", ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._update_photo
        return self

    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"incorrect api token")

    def validate_slug(self):
        if not Photo.objects.filter(slug=self.cleaned_data['slug'],
                                    user_id=self.cleaned_data['user_id']):
            raise ValidationError404(f"Incorrect slug value", code='invalid')

    def set_new_photo_name(self, value):
        self.cleaned_data['photo'].name = self.slug_russian_word(value)

    @property
    def validate_type_of_photo(self):
        if self.cleaned_data['photo'].content_type.split('/')[1] != 'jpeg':
            raise ValidationError409(f"Incorrect type of photo,try jpeg", code='invalid')

    @property
    def validate_photo_name(self):
        if Photo.objects.filter(photo_name=self.cleaned_data['photo_name']):
            raise ValidationError409(f"Photo with that name already exists", code='invalid')
        if Photo.objects.filter(slug=self.slug_russian_word(self.cleaned_data['photo_name'])):
            raise ValidationError409(f"Photo with that slug already exists, try new photo name", code='invalid')

    @property
    def _update_photo(self):
        post = Photo.objects.get(slug=self.cleaned_data['slug'])

        if self.cleaned_data['photo'] and self.cleaned_data['photo'] != post.photo:
            self.validate_type_of_photo
            self.set_new_photo_name(post.photo_name)
            post.previous_photo = post.photo
            post.photo = self.cleaned_data['photo']
            post.moderation = 'MOD'
        if self.cleaned_data['photo_name'] and self.cleaned_data['photo_name'] != post.photo_name:
            self.validate_photo_name
            post.photo_name = self.cleaned_data['photo_name']
            post.slug = self.slug_russian_word(self.cleaned_data['photo_name'])
        if self.cleaned_data['photo_content'] and self.cleaned_data['photo_content'] != post.photo_content:
            post.photo_content = self.cleaned_data['photo_content']
        post.save()
        return post
