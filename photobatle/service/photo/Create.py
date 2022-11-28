from transliterate import translit
from django import forms
from service_objects.services import ServiceWithResult
from photobatle.utils import *
from photobatle.models import *
from api.status_code import *


class AddPhotoService(DataMixin, ServiceWithResult):
    """Service class for add photo"""

    name = forms.CharField()
    content = forms.CharField()
    photo = forms.ImageField()
    user_id = forms.IntegerField()

    custom_validations = ["validate_type_of_photo", "validate_name", "validate_slug"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._create_photo
        return self

    @property
    def _create_photo(self):
        return Photo.objects.create(photo_name=self.cleaned_data['name'],
                                    photo_content=self.cleaned_data['content'],
                                    photo=self.cleaned_data['photo'],
                                    user_id=self.cleaned_data['user_id'],
                                    slug=self.cleaned_data['slug'])

    def validate_type_of_photo(self):
        if self.cleaned_data['photo'].content_type.split('/')[1] != 'jpeg':
            self.errors['type'] = "Incorrect type of photo,try jpeg"

    def validate_name(self):
        if not self.get_photo_objects_by_filter(photo_name=self.cleaned_data['name']):
            return self.set_slug()
        self.errors['name'] = "Photo with that name already exists"

    def validate_slug(self):
        if 'slug' in self.cleaned_data:
            if self.get_photo_objects_by_filter(slug=self.cleaned_data['slug']):
                self.errors['conflict_slug'] = "Photo with that slug already exists, try new photo name"

    @staticmethod
    def get_photo_objects_by_filter(**kwargs):
        return Photo.objects.filter(**kwargs)

    def set_slug(self):
        self.cleaned_data['slug'] = self.slug_russian_word(self.cleaned_data['name'])
        if self.cleaned_data['slug']:
            return self.set_photo_name()
        self.errors['name'] = "Incorrect name of photo"

    def set_photo_name(self):
        self.cleaned_data['photo'].name = translit(self.cleaned_data['photo'].name, 'ru', reversed=True)
