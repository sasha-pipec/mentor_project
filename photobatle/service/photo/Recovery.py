from functools import lru_cache

from django import forms
from service_objects.services import ServiceWithResult
from photobatle.celery import app
from photobatle.models import *
from api.status_code import *


class RecoveryPhotoService(ServiceWithResult):
    """Service class for recovery photo"""

    slug = forms.SlugField()
    user_id = forms.IntegerField(required=False)

    custom_validations = ["validate_user_id", "validate_slug", ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._recovery_photo
        return self

    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"incorrect api token")

    def validate_slug(self):
        try:
            return Photo.objects.get(slug=self.cleaned_data['slug'], user_id=self.cleaned_data['user_id'],
                                     moderation='DEL')
        except:
            raise ValidationError404(f"Incorrect slug value", code='invalid')

    @property
    def _recovery_photo(self):
        photo = Photo.objects.get(slug=self.cleaned_data['slug'])
        app.control.revoke(photo.task_id)
        photo.moderation = 'MOD'
        photo.save()
        return photo
