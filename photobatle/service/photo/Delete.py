from django import forms
from photobatle import models
from service_objects.services import Service
from photobatle import tasks


class DeletePhotoService(Service):
    """Service class for delete photo"""

    slug_id = forms.SlugField()
    user_id = forms.IntegerField()

    @property
    def validate_slug_id(self):
        try:
            models.Photomodels.Photo.objects.get(slug=self.cleaned_data['slug_id'],
                                                 user_id=self.cleaned_data['user_id'])
            return True
        except:
            raise Exception(f"Incorrect slug_id value")

    def process(self):
        if self.validate_slug_id:
            photo = models.Photomodels.Photo.objects.get(slug=self.cleaned_data['slug_id'])
            photo.moderation = 'DEL'
            tasks.delete_photo.s(slug=self.cleaned_data['slug_id']).apply_async(countdown=20, task_id=photo.slug)
            photo.save()
