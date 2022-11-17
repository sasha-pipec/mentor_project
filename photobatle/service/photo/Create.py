from django import forms
from service_objects.services import ServiceWithResult
from photobatle.utils import *
from photobatle.models import *
from api.status_code import *


class AddPhotoService(DataMixin, ServiceWithResult):
    """Service class for add photo"""

    name = forms.CharField(required=False)
    content = forms.CharField(required=False)
    photo = forms.Field(required=False)
    user_id = forms.IntegerField(required=False)

    custom_validations = ["validate_user_id", "validate_type_of_photo", "validate_name", "validate_content",
                          "validate_slug"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._create_photo
        return self

    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError400(f"Missing one of all requirements parameters: api token")

    def validate_type_of_photo(self):
        if not self.cleaned_data['photo']:
            raise ValidationError400(f"Missing one of all requirements parameters: photo")
        elif self.cleaned_data['photo'].content_type.split('/')[1] != 'jpeg':
            raise ValidationError409(f"Incorrect type of photo,try jpeg", code='invalid')

    def validate_name(self):
        if not self.cleaned_data['name']:
            raise ValidationError400(f"Missing one of all requirements parameters: name")
        elif Photo.objects.filter(photo_name=self.cleaned_data['name']):
            raise ValidationError409(f"Photo with that name already exists", code='invalid')
        self.set_new_photo_slug()
        self.set_new_photo_name()

    def validate_content(self):
        if not self.cleaned_data['content']:
            raise ValidationError400(f"Missing one of all requirements parameters: content")

    def validate_slug(self):
        if Photo.objects.filter(slug=self.cleaned_data['slug']):
            raise ValidationError409(f"Photo with that slug already exists, try new photo name", code='invalid')

    def set_new_photo_name(self):
        self.cleaned_data['photo'].name = self.cleaned_data['slug']

    def set_new_photo_slug(self):
        self.cleaned_data['slug'] = self.slug_russian_word(self.cleaned_data['name'])
        if not self.cleaned_data['slug']:
            raise ValidationError400(f"Incorrect name of photo", code='invalid')

    @property
    def _create_photo(self):
        return Photo.objects.create(photo_name=self.cleaned_data['name'],
                                    photo_content=self.cleaned_data['content'],
                                    photo=self.cleaned_data['photo'],
                                    user_id=self.cleaned_data['user_id'],
                                    slug=self.cleaned_data['slug'])
