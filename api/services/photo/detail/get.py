from django import forms

from service_objects.services import ServiceWithResult

from api.repositorys import *
from api.status_code import *
from photobatle.models import *


class GetDetailPhotoService(ServiceWithResult):
    """Service class for sorting form"""

    slug = forms.SlugField(required=False)
    user_id = forms.Field(required=False)

    custom_validations = ["validate_slug"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._get_detail_photo
        return self

    @property
    def _get_detail_photo(self):
        like = self._is_liked_by_current_user if self.cleaned_data['user_id'] else 'user_not_authenticate'
        return DetailPhotoRepository.get_object(like=like, moderation=Photo.APPROVED, slug=self.cleaned_data['slug'])

    def validate_slug(self):
        if not self.cleaned_data['slug']:
            raise ValidationError400(f'Missing one of all requirements parameters: slug')

    @property
    def _is_liked_by_current_user(self):
        photo = PhotoRepository.get_first_object_by_filter(slug=self.cleaned_data['slug'], moderation=Photo.APPROVED)
        if photo:
            like = LikeRepository.get_objects_by_filter(photo_id=photo.pk, user_id=self.cleaned_data['user_id'])
            return bool(like) if photo.user.pk != self.cleaned_data['user_id'] else 'you_author_of_this_photo'
        return False
