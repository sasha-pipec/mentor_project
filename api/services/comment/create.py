from functools import lru_cache

from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from photobatle.models import Comment, User, Photo


class ApiCreateCommentService(ServiceWithResult):
    """Service class for create comment"""

    comment = forms.CharField(required=False)
    parent_comment_id = forms.Field(required=False)
    slug = forms.SlugField(required=False)
    user = ModelField(User, required=False)

    custom_validations = ["check_required_parameters_presence", "check_photo_presence_by_slug"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.check_comment_presence_by_parent_id()
            if self.is_valid():
                self.result = self._created_comment
        return self

    @property
    def _created_comment(self):
        comment = Comment(
            photo=Photo(id=(self.check_photo_presence_by_slug()).id),
            user_id=self.cleaned_data['user'].id,
            parent_id=self.cleaned_data['parent_comment_id'],
            content=self.cleaned_data['comment']
        )
        comment.save()
        return comment

    def check_required_parameters_presence(self):
        fields = ['comment', 'user', 'slug']
        for field in fields:
            if not self.cleaned_data[field]:
                field = field if field != 'user' else 'api token'
                self.errors[field] = f"Missing one of all requirements parameters:{field}"

    @lru_cache()
    def check_photo_presence_by_slug(self):
        photo = Photo.objects.filter(slug=self.cleaned_data['slug'])
        if photo:
            return photo.first()
        self.errors['photo_not_found'] = f"Photo with slug '{self.cleaned_data['slug']}' not found"

    def check_comment_presence_by_parent_id(self):
        if self.cleaned_data['parent_comment_id']:
            comment = Comment.objects.filter(photo_id=(self.check_photo_presence_by_slug()).id,
                                             pk=self.cleaned_data['parent_comment_id'])
            if comment:
                return comment.first()
            self.errors['parent_not_found'] = f"Parent comment with id '{self.cleaned_data['parent_comment_id']}'" \
                                              " not found"
        self.cleaned_data['parent_comment_id'] = None
