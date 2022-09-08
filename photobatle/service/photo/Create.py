from django import forms
from service_objects.services import Service
from photobatle.utils import *
from django.core.exceptions import ValidationError
from photobatle.models import *


class AddPhotoService(DataMixin, Service):
    """Service class for add photo"""

    photo_name = forms.CharField()
    photo_content = forms.CharField()
    photo = forms.Field()
    user_id = forms.IntegerField()

    @property
    def validate_type_of_photo(self):
        if self.cleaned_data['photo'].content_type.split('/')[1] != 'jpeg':
            raise ValidationError(f"Incorrect type of photo,try jpeg", code='invalid')
        return True

    @property
    def validate_photo_name(self):
        if Photo.objects.filter(photo_name=self.cleaned_data['photo_name']):
            raise ValidationError(f"Photo with that name already exists", code='invalid')
        return True

    def get_new_photo_name(self):
        self.cleaned_data['photo'].name = self.slug_russian_word(self.cleaned_data['photo_name'])

    def process(self):
        if self.validate_type_of_photo:
            if self.validate_photo_name:
                self.get_new_photo_name()
                self.cleaned_data['slug'] = self.slug_russian_word(self.cleaned_data['photo_name'])
                Photo.objects.create(
                    **self.cleaned_data
                )