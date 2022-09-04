from django import forms
from service_objects.services import Service
from photobatle.celery import app
from django.core.exceptions import ValidationError
from photobatle.models import *


class RecoveryPhotoService(Service):
    """Service class for recovery photo"""

    slug = forms.SlugField()
    user_id = forms.IntegerField()

    def validate_slug_id(self):
        try:
            return Photo.objects.get(slug=self.cleaned_data['slug'],
                                     user_id=self.cleaned_data['user_id'],
                                     moderation='DEL')
        except:
            raise ValidationError(f"Incorrect slug value", code='invalid')

    def process(self):
        if self.validate_slug_id:
            photo = Photo.objects.get(slug=self.cleaned_data['slug'])
            app.control.revoke(photo.task_id)
            photo.moderation = 'MOD'
            photo.save()
