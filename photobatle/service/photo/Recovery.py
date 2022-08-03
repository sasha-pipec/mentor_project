from django import forms
from photobatle import models
from service_objects.services import Service
from photobatle.celery import app


class RecoveryPhotoService(Service):
    """Service class for recovery photo"""

    slug_id = forms.SlugField()

    def process(self):
        app.control.revoke(self.cleaned_data['slug_id'])
        photo = models.Photomodels.Photo.objects.get(slug=self.cleaned_data['slug_id'])
        photo.moderation = '2'
        photo.save()
