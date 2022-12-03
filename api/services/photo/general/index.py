from django import forms
from django.core.paginator import Paginator, EmptyPage
from service_objects.services import ServiceWithResult

from api.repositorys import GeneralPhotoRepository
from api.constants import *

from photobatle.models import Photo

from mentor_prooject.settings import REST_FRAMEWORK


class ListGeneralPhotoService(ServiceWithResult):
    """Api service class for det general photo"""

    page = forms.IntegerField(required=False)
    per_page = forms.IntegerField(required=False)
    sort_value = forms.CharField(required=False)
    search_value = forms.CharField(required=False)
    direction = forms.CharField(required=False)

    custom_validations = ["validate_sort_value", "validate_direction"]

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
    def _photos(self):
        return GeneralPhotoRepository.get_objects_by_filter_with_order(
            search_value=self.cleaned_data['search_value'],
            sort_value=self.cleaned_data['sort_value'],
            moderation=Photo.APPROVED)

    def validate_direction(self):
        if self.cleaned_data['direction'] and self.cleaned_data['direction'] not in DIRECTION_LIST:
            self.errors['direction'] = f"Incorrect direction '{self.cleaned_data['direction']}'"
        if self.cleaned_data['direction'] == 'desc' and self.cleaned_data['sort_value'] != DEFAULT_SORT_VALUE:
            self.cleaned_data['sort_value'] = "-" + self.cleaned_data['sort_value']

    def validate_sort_value(self):
        self.cleaned_data['sort_value'] = self.cleaned_data['sort_value'] or DEFAULT_SORT_VALUE
        if self.cleaned_data['sort_value'] not in SORT_LIST:
            self.errors['sort_value'] = f"Incorrect sort_value '{self.cleaned_data['sort_value']}'"