from functools import lru_cache

from django import forms
from django.db.models import Count, Value

from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField

from api.status_code import ValidationError400, ValidationError404
from photobatle.models import Photo, User, Like


class ShowDetailPhotoService(ServiceWithResult):
    """Service class for sorting form"""

    slug = forms.SlugField(required=False)
    user = ModelField(User, required=False)

    custom_validations = ["check_slug_presence", ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            if self._photo_presence:
                self.result = self._get_detail_photo
        return self

    @property
    def _get_detail_photo(self):
        like = self._is_liked_by_current_user if self.cleaned_data['user'] else False
        photo = self._photo_presence
        photo.is_liked_by_current_user = like
        photo.save()
        return photo

    def check_slug_presence(self):
        if not self.cleaned_data['slug']:
            raise ValidationError400(f'Missing one of all requirements parameters: slug')

    @property
    @lru_cache
    def _photo_presence(self):
        try:
            return Photo.objects.annotate(is_liked_by_current_user=Value(False)).get(
                slug=self.cleaned_data['slug'], moderation=Photo.APPROVED
            )
        except Exception:
            raise ValidationError404("Photo by this slug not found")

    @property
    def _is_liked_by_current_user(self):
        photo = self._photo_presence
        like = Like.objects.filter(photo_id=photo.pk, user_id=self.cleaned_data['user'].pk)
        return bool(like) if self._photo_presence.user.pk != self.cleaned_data['user'].id else False
