from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField

from photobatle.utils import DataMixin
from photobatle.models import Photo, User


class ApiAddPhotoService(DataMixin, ServiceWithResult):
    """API service class for add photo"""

    name = forms.CharField(required=False)
    content = forms.CharField(required=False)
    photo = forms.ImageField(required=False)
    user = ModelField(User, required=False)

    custom_validations = ["validate_type_of_photo"]

    def process(self):
        self.check_required_parameters_presence()
        if self.is_valid():
            self.run_custom_validations()
            if self.is_valid():
                self.result = self._create_photo
        return self

    @property
    def _create_photo(self) -> Photo:
        photo = Photo(photo_name=self.cleaned_data['name'],
                      photo_content=self.cleaned_data['content'],
                      photo=self.cleaned_data['photo'],
                      user_id=self.cleaned_data['user'].id, )
        photo.save()
        return photo

    def check_required_parameters_presence(self):
        for field in self.fields:
            if not self.cleaned_data[str(field)]:
                field = field if field != 'user' else 'api token'
                self.errors[field] = f"Missing one of all requirements parameters:{str(field)}"

    def validate_type_of_photo(self):
        type_of_photo = self.cleaned_data['photo'].content_type.split('/')[1]
        if type_of_photo != 'jpeg':
            self.errors['type'] = f"Incorrect type of photo '{type_of_photo}',try jpeg"
