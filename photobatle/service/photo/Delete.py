from django import forms
from photobatle import models
from service_objects.services import Service
from photobatle import tasks


class DeletePhotoService(Service):
    """Service class for delete photo"""

    slug_id = forms.SlugField()

    def process(self):
        photo = models.Photomodels.Photo.objects.get(slug=self.cleaned_data['slug_id'])
        photo.moderation = 'DEL'
        tasks.delete_photo.s(slug=self.cleaned_data['slug_id']).apply_async(countdown=20, task_id=photo.slug)
        photo.save()
