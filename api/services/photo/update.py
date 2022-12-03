from functools import lru_cache

from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField

from photobatle.utils import DataMixin
from photobatle.models import Photo, User


class ApiUpdatePhotoService(DataMixin, ServiceWithResult):
    """Service class for update photo"""

    slug = forms.SlugField(required=False)
    name = forms.CharField(required=False)
    content = forms.CharField(required=False)
    photo = forms.ImageField(required=False)
    user = ModelField(User)

    custom_validations = ["check_required_parameters_presence", "_photo_presence", "check_type_of_photo_file"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._update_photo
        return self

    @property
    def _update_photo(self) -> Photo:
        post = self._photo_presence()

        if self.cleaned_data['photo'] and self.cleaned_data['photo'] != post.photo:
            post.previous_photo = post.photo
            post.photo = self.cleaned_data['photo']
            post.moderation = Photo.ON_MODERATION
        if self.cleaned_data['name'] and self.cleaned_data['name'] != post.photo_name:
            post.photo_name = self.cleaned_data['name']
        if self.cleaned_data['content'] and self.cleaned_data['content'] != post.photo_content:
            post.photo_content = self.cleaned_data['content']
        post.save()
        return post

    def check_required_parameters_presence(self):
        required_fields = ['user', 'slug']
        for field in required_fields:
            if not self.cleaned_data[field]:
                field = field if field != 'user' else 'api token'
                self.errors[field] = f"Missing one of all requirements parameters: {field}"

    @lru_cache
    def _photo_presence(self):
        try:
            return Photo.objects.get(slug=self.cleaned_data['slug'], user_id=self.cleaned_data['user'].id)
        except Exception:
            self.errors['object_not_found'] = f"Photo with slug '{self.cleaned_data['slug']}' not found"

    def check_type_of_photo_file(self):
        if self.cleaned_data['photo'] and self.cleaned_data['photo'].content_type.split('/')[1] != 'jpeg':
            self.errors['type'] = "Incorrect type of photo,try jpeg"
