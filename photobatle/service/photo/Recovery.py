from django import forms
from service_objects.services import Service
from photobatle.celery import app
from photobatle.models import *
from api.status_code import *


class RecoveryPhotoService(Service):
    """Service class for recovery photo"""

    slug = forms.SlugField()
    user_id = forms.IntegerField(required=False)

    def process(self):
        self.validate_user_id
        self.validate_slug_id
        photo = Photo.objects.get(slug=self.cleaned_data['slug'])
        app.control.revoke(photo.task_id)
        photo.moderation = 'MOD'
        photo.save()

    @property
    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"incorrect api token")

    def validate_slug_id(self):
        try:
            return Photo.objects.get(slug=self.cleaned_data['slug'],
                                     user_id=self.cleaned_data['user_id'],
                                     moderation='DEL')
        except:
            raise ValidationError400(f"Incorrect slug value", code='invalid')