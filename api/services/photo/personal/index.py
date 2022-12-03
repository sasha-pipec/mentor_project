from functools import lru_cache

from django import forms
from django.core.paginator import Paginator, EmptyPage
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField

from api.repositorys import PersonalPhotoRepository
from api.status_code import ValidationError401, ValidationError400
from api.constants import *
from mentor_prooject.settings import REST_FRAMEWORK

from photobatle.models import Photo, User


class PersonalListPhotoService(ServiceWithResult):
    """Service class for sorting form"""

    page = forms.IntegerField(required=False)
    per_page = forms.IntegerField(required=False)
    sort_value = forms.CharField(required=False)
    user = ModelField(User, required=False)

    custom_validations = ["check_user_presence", "validate_sort_value"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._paginated_photos
        return self

    @property
    def _paginated_photos(self):
        try:
            return Paginator(
                self._photos,
                self.cleaned_data["per_page"] or REST_FRAMEWORK["PAGE_SIZE"],
            ).page(self.cleaned_data["page"] or 1)
        except EmptyPage:
            return Paginator(
                Photo.objects.none(),
                self.cleaned_data["per_page"] or REST_FRAMEWORK["PAGE_SIZE"],
            ).page(1)

    @property
    @lru_cache
    def _photos(self):
        return PersonalPhotoRepository.get_objects_by_filter(sort_value=self.cleaned_data['sort_value'],
                                                             user_id=self.cleaned_data['user'].pk)

    def check_user_presence(self):
        if not self.cleaned_data['user']:
            raise ValidationError401(f"Missing one of all requirements parameters: api token")

    def validate_sort_value(self):
        if self.cleaned_data['sort_value'] and self.cleaned_data['sort_value'] not in STATUS_LIST:
            raise ValidationError400(f"Incorrect value of sorting")
