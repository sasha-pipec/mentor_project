from functools import lru_cache

from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from photobatle.celery import app
from photobatle.models import Photo, User


class ApiRecoveryPhotoService(ServiceWithResult):
    """Service class for recovery photo"""

    slug = forms.SlugField(required=False)
    user = ModelField(User, required=False)

    custom_validations = ["check_required_parameters_presence", "_photo_presence", ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._recovery_photo
        return self

    @property
    def _recovery_photo(self) -> Photo:
        photo = self._photo_presence()
        app.control.revoke(photo.task_id)
        photo.moderation = Photo.ON_MODERATION
        photo.save()
        return photo

    def check_required_parameters_presence(self):
        required_fields = ['user', 'slug']
        for field in required_fields:
            if not self.cleaned_data[field]:
                field = field if field != 'user' else 'api token'
                self.errors[field] = f"Missing one of all requirements parameters: {field}"

    @lru_cache
    def _photo_presence(self):
        try:
            return Photo.objects.get(slug=self.cleaned_data['slug'], user_id=self.cleaned_data['user'].id,
                                     moderation=Photo.ON_DELETION)
        except Exception:
            self.errors['object_not_found'] = f"Photo with slug '{self.cleaned_data['slug']}' not found"
