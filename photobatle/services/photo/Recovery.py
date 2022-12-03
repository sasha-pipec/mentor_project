from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from photobatle.celery import app
from photobatle.models import Photo, User


class RecoveryPhotoService(ServiceWithResult):
    """Service class for recovery photo"""

    slug = forms.SlugField()
    user = ModelField(User)

    def process(self):
        self.result = self._recovery_photo
        return self

    @property
    def _recovery_photo(self) -> Photo:
        photo = Photo.objects.get(slug=self.cleaned_data['slug'])
        app.control.revoke(photo.task_id)
        photo.moderation = Photo.ON_MODERATION
        photo.save()
        return photo
