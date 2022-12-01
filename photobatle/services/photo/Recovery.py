from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from photobatle.celery import app
from photobatle.models import Photo, User
from api.status_code import *


class RecoveryPhotoService(ServiceWithResult):
    """Service class for recovery photo"""

    slug = forms.SlugField()
    user = ModelField(User)

    custom_validations = ["validate_user", "validate_slug", ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._recovery_photo
        return self

    @property
    def _recovery_photo(self):
        photo = Photo.objects.get(slug=self.cleaned_data['slug'])
        app.control.revoke(photo.task_id)
        photo.moderation = Photo.ON_MODERATION
        photo.save()
        return photo

    def validate_user(self):
        if not self.cleaned_data['user']:
            raise ValidationError401("Missing one of all requirements parameters: api_token")

    def validate_slug(self):
        try:
            return Photo.objects.get(slug=self.cleaned_data['slug'], user_id=self.cleaned_data['user'].id,
                                     moderation=Photo.ON_DELETION)
        except Exception:
            raise ValidationError404(f"Incorrect slug value", code='invalid')
