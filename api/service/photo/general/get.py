from django import forms
from django.core.paginator import Paginator
from django.db.models import Q, Count
from service_objects.services import ServiceWithResult
from photobatle.models import *
from api.status_code import *
from api.utils import *


class GetPhotoService(ServiceWithResult):
    """Service class for sorting form"""

    page = forms.IntegerField(required=False)
    sort_value = forms.CharField(required=False)
    search_value = forms.CharField(required=False)
    direction = forms.CharField(required=False)

    custom_validations = ["validate_sort_value", "validate_direction"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._get_photo_on_page
        return self

    def validate_direction(self):
        directions = ['asc', 'desc']
        if self.cleaned_data['direction']:
            if self.cleaned_data['direction'] not in directions:
                raise ValidationError404(f"Incorrect direction")
            if self.cleaned_data['direction'] == 'desc':
                self.cleaned_data['sort_value'] = "-" + self.cleaned_data['sort_value']
                return
        self.cleaned_data['direction'] = 'asc'

    def validate_sort_value(self):
        sort_list = ['like_count', 'comment_count', 'updated_at', 'id']
        if self.cleaned_data['sort_value'] and self.cleaned_data['sort_value'] not in sort_list:
            raise ValidationError404(f"Incorrect sort_value")
        elif not self.cleaned_data['sort_value']:
            self.cleaned_data['sort_value'] = "id"

    def validate_page(self, page_range):
        if not self.cleaned_data['page']:
            self.cleaned_data['page'] = 1
        if self.cleaned_data['page'] >= page_range.stop:
            raise ValidationError404(f"Incorrect page")

    @property
    def _get_photo_on_page(self):
        all_photos = Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                            like_count=Count('like_photo', distinct=True)).filter(
            Q(user__username__icontains=self.cleaned_data['search_value']) |
            Q(photo_name__icontains=self.cleaned_data['search_value']) |
            Q(photo_content__icontains=self.cleaned_data['search_value']),
            moderation='APR').order_by(self.cleaned_data['sort_value'])
        paginator = Paginator(all_photos, 4)
        self.validate_page(paginator.page_range)
        pagination_data = CustomPagination(paginator.get_page(self.cleaned_data['page']), self.cleaned_data['page'],
                                           paginator.per_page)
        photos_on_page = (paginator.page(int(self.cleaned_data['page']))).object_list
        return {'photos': photos_on_page, 'pagination_data': pagination_data.to_json()}
