from django import forms
from service_objects.services import Service
from photobatle.utils import *
from django.core.exceptions import ValidationError


class UpdatePhotoService(DataMixin, Service):
    """Service class for update photo"""

    def get_type_of_photo(self):
        if self.file:
            if self.content_type.split('/')[1] != 'jpeg':
                raise ValidationError('Тип загружаемого файла не JPEG, повторите попытку', code='invalid')
        return None

    slug_id = forms.SlugField()
    photo_name = forms.CharField()
    photo_content = forms.CharField()
    photo = forms.Field(required=False, validators=[get_type_of_photo])

    def process(self):
        post = models.Photomodels.Photo.objects.get(slug=self.cleaned_data['slug_id'])

        if self.cleaned_data['photo']:
            post.photo = self.cleaned_data['photo']
        post.photo_name = self.cleaned_data['photo_name']
        post.photo_content = self.cleaned_data['photo_content']
        post.slug = self.slug_russian_word(self.cleaned_data['photo_name'])
        return post.save()
