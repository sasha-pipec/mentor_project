from functools import lru_cache

from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField

from photobatle import tasks
from photobatle.models import Photo, User


class ApiDeletePhotoService(ServiceWithResult):
    """Service class for delete photo"""

    slug = forms.SlugField(required=False)
    user = ModelField(User, required=False)

    custom_validations = ["check_required_parameters_presence", "_photo_presence", ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._delete_photo
        return self

    @property
    def _delete_photo(self):
        photo = self._photo_presence()
        photo.moderation = Photo.ON_DELETION
        task = tasks.delete_photo.s(photo.slug).apply_async(countdown=20)
        photo.task_id = task.id
        photo.save()

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
