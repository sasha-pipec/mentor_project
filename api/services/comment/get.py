from django import forms
from service_objects.services import ServiceWithResult

from api.status_code import *
from api.utils import can_be_deleted_and_changing_by_user
from api.repositorys import *
from photobatle.models import *


class GetCommentForPhotoService(ServiceWithResult):
    """Service class for sorting form"""

    slug = forms.SlugField(required=False)
    user_id = forms.IntegerField(required=False)

    custom_validations = ["validate_slug"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._get_comments_for_photo
        return self

    def validate_slug(self):
        if not PhotoRepository.get_objects_by_filter(slug=self.cleaned_data['slug']):
            if not self.cleaned_data['slug']:
                raise ValidationError400(f'Missing one of all requirements parameters: slug')
            raise ValidationError404(f"Incorrect slug value")

    @property
    def _get_comments_for_photo(self):
        photo = PhotoRepository.get_first_object_by_filter(slug=self.cleaned_data['slug'])
        comments = CommentRepository.get_objects_by_filter(photo_id=photo.id, parent=None)
        if self.cleaned_data['user_id']:
            comments = can_be_deleted_and_changing_by_user(comments, self.cleaned_data['user_id'])
        return comments
