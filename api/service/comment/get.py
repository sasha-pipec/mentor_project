from django import forms
from django.db.models import Value
from service_objects.services import ServiceWithResult
from photobatle.models import *
from api.status_code import *
from api.utils import get_answers_for_comments


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
        try:
            Photo.objects.get(slug=self.cleaned_data['slug'])
        except Exception:
            if not self.cleaned_data['slug']:
                raise ValidationError400(f'Missing one of all requirements parameters: slug')
            raise ValidationError404(f"Incorrect slug value")

    @property
    def _get_comments_for_photo(self):
        photo = Photo.objects.get(slug=self.cleaned_data['slug'])
        comments = Comment.objects.filter(photo_id=photo.id,
                                          parent=None).annotate(removal=Value('user_not_authenticate'),
                                                                change=Value('user_not_authenticate'))
        if self.cleaned_data['user_id']:
            comments = get_answers_for_comments(comments,self.cleaned_data['user_id'])
        return comments
