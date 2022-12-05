from functools import lru_cache

from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField

from api.repositorys import PhotoRepository, LikeRepository
from photobatle.models import Like, Photo, User


class ApiLikeToggleService(ServiceWithResult):
    """Api service class for create/delete like"""

    slug = forms.SlugField(required=False)
    user = ModelField(User, required=False)

    custom_validations = ["check_required_parameters_presence", "check_photo_presence_by_slug", ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            if self.check_like_presence:
                self.result = self._like_deleted
            else:
                self.check_author_of_photo()
                if self.is_valid():
                    self.result = self._like_created
        return self

    @property
    def _like_deleted(self):
        like = self.check_like_presence
        like.delete()
        return False

    @property
    def _like_created(self):
        like = Like(photo_id=self.check_photo_presence_by_slug.id, user_id=self.cleaned_data['user_id'])
        like.save()
        return True

    def check_required_parameters_presence(self):
        for field in self.fields:
            if not self.cleaned_data[str(field)]:
                field = field if field != 'user' else 'api token'
                self.errors[field] = f"Missing one of all requirements parameters:{str(field)}"

    @lru_cache
    def check_photo_presence_by_slug(self) -> Photo:
        photo = PhotoRepository.get_objects_by_filter(slug=self.cleaned_data['slug'])
        if photo:
            return photo.first()
        self.errors['not_found'] = f"Photo with slug '{self.cleaned_data['slug']}' not found"

    @property
    @lru_cache
    def check_like_presence(self) -> Like:
        like = LikeRepository.get_objects_by_filter(user_id=self.cleaned_data['user'].id,
                                                    photo_id=self.check_photo_presence_by_slug().id)
        return like

    def check_author_of_photo(self):
        if self.check_photo_presence_by_slug().user == self.cleaned_data['user']:
            self.errors['conflict'] = "You can't like this photo, because it is your photo"
