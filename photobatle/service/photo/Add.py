from django import forms
from service_objects.services import Service
from photobatle.utils import *
from django.core.exceptions import ValidationError


class AddPhotoService(DataMixin, Service):
    """Service class for add photo"""

    def get_type_of_photo(self):
        if self.content_type.split('/')[1] != 'jpeg':
            raise ValidationError('Тип загружаемого файла не JPEG, повторите попытку', code='invalid')

    photo_name = forms.CharField()
    photo_content = forms.CharField()
    photo = forms.Field(validators=[get_type_of_photo])
    user_id = forms.IntegerField()

    def process(self):
        return models.Photomodels.Photo.objects.create(
            photo_name=self.cleaned_data['photo_name'],
            photo_content=self.cleaned_data['photo_content'],
            photo=self.cleaned_data['photo'],
            user_id=self.cleaned_data['user_id'],
            slug=self.slug_russian_word(self.cleaned_data['photo_name'])
        )
