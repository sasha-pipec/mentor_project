from django import forms
from django.core.paginator import Paginator
from django.db.models import Count
from service_objects.services import ServiceWithResult

from api.utils import CustomPagination
from photobatle.models import *
from api.status_code import *


class GetPersonalPhotoService(ServiceWithResult):
    """Service class for sorting form"""

    page = forms.IntegerField(required=False)
    sort_value = forms.CharField(required=False)
    user_id = forms.IntegerField(required=False)

    custom_validations = ["validate_user_id", "validate_sort_value"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._get_photo_on_page
        return self

    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"Missing one of all requirements parameters: api token")

    def validate_sort_value(self):
        sort_list = ['DEL', 'MOD', 'APR', 'REJ']
        if self.cleaned_data['sort_value'] and self.cleaned_data['sort_value'] not in sort_list:
            raise ValidationError404(f"Incorrect sort_value")

    def validate_page(self, page_range):
        if not self.cleaned_data['page']:
            self.cleaned_data['page'] = 1
        if self.cleaned_data['page'] >= page_range.stop:
            raise ValidationError404(f"Incorrect page")

    @property
    def _get_photo_on_page(self):
        if self.cleaned_data['sort_value']:
            all_photos = Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                like_count=Count('like_photo', distinct=True)).filter(
                user_id=self.cleaned_data['user_id'], moderation=self.cleaned_data['sort_value'])
        else:
            all_photos = Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                like_count=Count('like_photo', distinct=True)).filter(
                user_id=self.cleaned_data['user_id'])
        paginator = Paginator(all_photos, 4)
        self.validate_page(paginator.page_range)
        pagination_data = CustomPagination(paginator.get_page(self.cleaned_data['page']), self.cleaned_data['page'],
                                           paginator.per_page)
        photos_on_page = (paginator.page(int(self.cleaned_data['page']))).object_list
        return {'photos': photos_on_page, 'pagination_data': pagination_data.to_json()}
