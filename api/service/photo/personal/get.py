from django import forms
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Count
from service_objects.services import ServiceWithResult

from api.utils import CustomPagination
from api.status_code import *
from api.repositorys import *
from api.constants import *
from mentor_prooject.settings import REST_FRAMEWORK

from photobatle.models import *


class GetPersonalPhotoService(ServiceWithResult):
    """Service class for sorting form"""

    page = forms.IntegerField(required=False)
    per_page = forms.IntegerField(required=False)
    sort_value = forms.CharField(required=False)
    user_id = forms.IntegerField(required=False)

    custom_validations = ["validate_user_id", "validate_sort_value"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._paginated_photos
        return self

    @property
    def _paginated_photos(self):
        try:
            paginator = Paginator(
                self._photos,
                self.cleaned_data["per_page"] or REST_FRAMEWORK["PAGE_SIZE"],
            ).page(self.cleaned_data["page"] or 1)
        except EmptyPage:
            paginator = Paginator(
                Photo.objects.none(),
                self.cleaned_data["per_page"] or REST_FRAMEWORK["PAGE_SIZE"],
            ).page(1)
        finally:
            pagination_data = CustomPagination(
                paginator,
                self.cleaned_data['page'],
                self.cleaned_data["per_page"] or REST_FRAMEWORK["PAGE_SIZE"]
            )
            return {'photos': paginator, 'pagination_data': pagination_data.to_json()}

    @property
    def _photos(self):
        return PersonalPhotoRepository.get_objects_by_filter(sort_value=self.cleaned_data['sort_value'],
                                                             user_id=self.cleaned_data['user_id'])

    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"Missing one of all requirements parameters: api token")

    def validate_sort_value(self):
        if self.cleaned_data['sort_value'] and self.cleaned_data['sort_value'] not in STATUS_LIST:
            raise ValidationError400(f"Incorrect sort_value")
