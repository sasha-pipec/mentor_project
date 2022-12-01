from functools import lru_cache

from django import forms
from service_objects.services import ServiceWithResult

from api.repositorys import PhotoRepository
from api.status_code import *
from photobatle.models import *


class ApiCreateLikeService(ServiceWithResult):
    """Api service class for create like"""

    slug = forms.SlugField(required=False)
    user_id = forms.IntegerField(required=False)

    custom_validations = ["validate_author_of_photo", ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._create_like
        return self

    @property
    def _create_like(self):
        Like.objects.create(photo_id=self._photo.id, user_id=self.cleaned_data['user_id'])
        return True

    @property
    @lru_cache
    def _photo(self):
        return PhotoRepository.get_first_object_by_filter(slug=self.cleaned_data['slug'])

    def validate_author_of_photo(self):
        if self._photo.user.id == self.cleaned_data['user_id']:
            raise ValidationError409("You can't like this photo, because it is your photo")
