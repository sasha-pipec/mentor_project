from django import forms
from service_objects.services import ServiceWithResult
from transliterate import translit

from api.repositorys import *
from photobatle.utils import DataMixin
from photobatle.models import *


class ApiAddPhotoService(DataMixin, ServiceWithResult):
    """API service class for add photo"""

    name = forms.CharField(required=False)
    content = forms.CharField(required=False)
    photo = forms.ImageField(required=False)
    user_id = forms.IntegerField(required=False)

    custom_validations = ["validate_type_of_photo", "validate_name", "validate_slug"]

    def process(self):
        self.validate_parameters()
        if self.is_valid():
            self.run_custom_validations()
            if self.is_valid():
                self.result = self._create_photo
        return self

    @property
    def _create_photo(self) -> Photo:
        return Photo.objects.create(photo_name=self.cleaned_data['name'],
                                    photo_content=self.cleaned_data['content'],
                                    photo=self.cleaned_data['photo'],
                                    user_id=self.cleaned_data['user_id'],
                                    slug=self.cleaned_data['slug'])

    def validate_parameters(self):
        for field in self.fields:
            if not self.cleaned_data[str(field)]:
                self.errors[str(field)] = f"Missing one of all requirements parameters:{str(field)}"

    def validate_type_of_photo(self):
        type_of_photo = self.cleaned_data['photo'].content_type.split('/')[1]
        if type_of_photo != 'jpeg':
            self.errors['type'] = f"Incorrect type of photo '{type_of_photo}',try jpeg"

    def validate_name(self):
        if not PhotoRepository.get_objects_by_filter(photo_name=self.cleaned_data['name']):
            return self.set_slug()
        self.errors['conflict_name'] = "Photo with that name already exists"

    def validate_slug(self):
        if 'slug' in self.cleaned_data:
            if PhotoRepository.get_objects_by_filter(slug=self.cleaned_data['slug']):
                self.errors['conflict_slug'] = "Photo with that slug already exists, try new photo name"

    def set_slug(self):
        self.cleaned_data['slug'] = self.slug_russian_word(self.cleaned_data['name'])
        if self.cleaned_data['slug']:
            return self.set_photo_name()
        self.errors['conflict_name'] = "Incorrect name of photo"

    def set_photo_name(self):
        self.cleaned_data['photo'].name = translit(self.cleaned_data['photo'].name, 'ru', reversed=True)
