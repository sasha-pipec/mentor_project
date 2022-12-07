from functools import lru_cache

from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField

from api.status_code import *
from api.utils import can_be_deleted_and_changing_by_user
from api.query_objects import PhotoRepository, CommentRepository
from photobatle.models import Comment, User


class ListCommentForPhotoService(ServiceWithResult):
    """Service class for sorting form"""

    slug = forms.SlugField(required=False)
    user = ModelField(User, required=False)

    custom_validations = ["check_slug_presence", "check_photo_presence_by_slug"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._get_comments_for_photo
        return self

    def check_slug_presence(self):
        if not self.cleaned_data['slug']:
            raise ValidationError400(f'Missing one of all requirements parameters: slug')

    @lru_cache
    def check_photo_presence_by_slug(self):
        photo = PhotoRepository.get_objects_by_filter(slug=self.cleaned_data['slug'])
        if not photo:
            raise ValidationError404(f"Photo with slug '{self.cleaned_data['slug']}' not found")
        return photo.first()

    @property
    def _get_comments_for_photo(self):
        photo = self.check_photo_presence_by_slug()
        comments = CommentRepository.get_objects_by_filter(photo_id=photo.id, parent=None)
        if self.cleaned_data['user'].id:
            comments = can_be_deleted_and_changing_by_user(comments, self.cleaned_data['user'].id)
        return comments
