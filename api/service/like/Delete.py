from django import forms
from service_objects.services import ServiceWithResult

from api.repositorys import PhotoRepository
from photobatle.models import *


class ApiDeleteLikeService(ServiceWithResult):
    """Service class for delete like"""

    slug = forms.SlugField(required=False)
    user_id = forms.IntegerField(required=False)

    def process(self):
        self.result = self._delete_like
        return self

    @property
    def _delete_like(self):
        photo = PhotoRepository.get_first_object_by_filter(slug=self.cleaned_data['slug'])
        Like.objects.get(photo_id=photo.id, user_id=self.cleaned_data['user_id']).delete()
        return False
