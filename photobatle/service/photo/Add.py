from django import forms
from service_objects.services import Service
from photobatle.utils import *
from django.core.exceptions import ValidationError


class AddPhotoService(DataMixin, Service):
    """Service class for add photo"""

    def get_type_of_photo(self):
        if self.content_type.split('/')[1] != 'jpeg':
            raise ValidationError(f"Incorrect type of photo,try jpeg", code='invalid')


    photo_name = forms.CharField()
    photo_content = forms.CharField()
    photo = forms.Field(validators=[get_type_of_photo])
    user_id = forms.IntegerField()


    def get_new_photo_name(self):
        self.cleaned_data['photo'].name = self.cleaned_data['photo_name']

    @property
    def validate_photo_name(self):
        try:
            models.Photomodels.Photo.objects.get(slug=self.slug_russian_word(self.cleaned_data['photo_name']))
            raise ValidationError(f"Incorrect photo_name value, field must be unique", code='invalid')
        except:
            return True

    def process(self):
        if self.validate_photo_name:
            self.get_new_photo_name()
            models.Photomodels.Photo.objects.create(
                photo_name=self.cleaned_data['photo_name'],
                photo_content=self.cleaned_data['photo_content'],
                photo=self.cleaned_data['photo'],
                user_id=self.cleaned_data['user_id'],
                slug=self.slug_russian_word(self.cleaned_data['photo_name'])
            )
