from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from photobatle.utils import DataMixin
from photobatle.models import Photo, User


class AddPhotoService(DataMixin, ServiceWithResult):
    """Service class for add photo"""

    name = forms.CharField()
    content = forms.CharField()
    photo = forms.ImageField()
    user = ModelField(User)

    custom_validations = ["validate_type_of_photo"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._create_photo
        return self

    @property
    def _create_photo(self):
        photo = Photo(photo_name=self.cleaned_data['name'],
                      photo_content=self.cleaned_data['content'],
                      photo=self.cleaned_data['photo'],
                      user_id=self.cleaned_data['user'].id, )
        photo.save()
        return photo

    def validate_type_of_photo(self):
        if self.cleaned_data['photo'].content_type.split('/')[1] != 'jpeg':
            self.errors['type'] = "Incorrect type of photo,try jpeg"
