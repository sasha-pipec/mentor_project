from django import forms
from django.db.models import Count, Value
from service_objects.services import ServiceWithResult
from photobatle.models import *
from api.status_code import *


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

    def validate_slug(self):
        try:
            Photo.objects.get(slug=self.cleaned_data['slug'], moderation='APR')
        except Exception:
            if not self.cleaned_data['slug']:
                raise ValidationError400(f'Missing one of all requirements parameters: slug')
            raise ValidationError404(f"Incorrect slug value")

    @property
    def _like_exist(self):
        photo = Photo.objects.get(slug=self.cleaned_data['slug'], moderation='APR')
        like = Like.objects.filter(photo_id=photo.id, user_id=self.cleaned_data['user_id'])
        return bool(like) if photo.user.pk != self.cleaned_data['user_id'] else 'you_author_of_this_photo'

    @property
    def _get_detail_photo(self):
        like = self._like_exist if self.cleaned_data['user_id'] else 'user_not_authenticate'
        return Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                      like_count=Count('like_photo', distinct=True),
                                      like_exist=Value(like)).get(moderation='APR', slug=self.cleaned_data['slug'])
