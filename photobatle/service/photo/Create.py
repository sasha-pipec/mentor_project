from django import forms
from service_objects.services import Service
from photobatle.utils import *
from photobatle.models import *
from api.status_code import *


class AddPhotoService(DataMixin, Service):
    """Service class for add photo"""

    photo_name = forms.CharField()
    photo_content = forms.CharField()
    photo = forms.Field()
    user_id = forms.IntegerField(required=False)

    def process(self):
        self.validate_user_id
        self.validate_type_of_photo
        self.validate_photo_name
        self.get_new_photo_slug()
        self.get_new_photo_name()
        self.validate_photo_slug
        Photo.objects.create(
            **self.cleaned_data
        )

    @property
    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"incorrect api token")

    @property
    def validate_type_of_photo(self):
        if self.cleaned_data['photo'].content_type.split('/')[1] != 'jpeg':
            raise ValidationError409(f"Incorrect type of photo,try jpeg", code='invalid')

    @property
    def validate_photo_name(self):
        if Photo.objects.filter(photo_name=self.cleaned_data['photo_name']):
            raise ValidationError409(f"Photo with that name already exists", code='invalid')

    @property
    def validate_photo_slug(self):
        if Photo.objects.filter(slug=self.cleaned_data['slug']):
            raise ValidationError409(f"Photo with that slug already exists, try new photo name", code='invalid')

    def get_new_photo_name(self):
        self.cleaned_data['photo'].name = self.cleaned_data['slug']

    def get_new_photo_slug(self):
        self.cleaned_data['slug'] = self.slug_russian_word(self.cleaned_data['photo_name'])
        if not self.cleaned_data['slug']:
            raise ValidationError400(f"Incorrect photo name", code='invalid')
