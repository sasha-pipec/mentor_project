from django import forms
from django.core.paginator import Paginator
from django.db.models import Count, Q
from service_objects.services import ServiceWithResult
from api.status_code import *
from photobatle.utils import *


class PaginationService(ServiceWithResult):
    """Service class for personal sorting form"""

    sort_value = forms.CharField(required=False)
    search_value = forms.CharField(required=False)
    direction = forms.CharField()
    page = forms.CharField()

    custom_validations = ["validate_sort_value", "validate_direction", ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._get_photo_on_page
        return self

    def validate_sort_value(self):
        sort_list = ['like_count', 'comment_count', 'updated_at', 'id']
        if not self.cleaned_data['sort_value']:
            self.cleaned_data['sort_value'] = 'id'
        if self.cleaned_data['sort_value'] not in sort_list:
            raise ValidationError404(f"Incorrect sort_value")

    def validate_direction(self):
        if self.cleaned_data['direction'] == 'desc':
            self.cleaned_data['sort_value'] = '-' + self.cleaned_data['sort_value']

    def validate_page(self, page_range):
        try:
            if int(self.cleaned_data['page']) >= page_range.stop:
                raise ValidationError404(f"Incorrect page")
        except Exception:
            raise ValidationError404(f"Incorrect page")

    @property
    def _get_photo_on_page(self):
        all_photos = Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                            like_count=Count('like_photo', distinct=True)).filter(
            Q(user__username__icontains=self.cleaned_data['search_value']) |
            Q(photo_name__icontains=self.cleaned_data['search_value']) |
            Q(photo_content__icontains=self.cleaned_data['search_value']),
            moderation='APR').order_by(self.cleaned_data['sort_value'])
        paginator = Paginator(all_photos, 2)
        self.validate_page(paginator.page_range)
        photos_on_page = (paginator.page(int(self.cleaned_data['page']))).object_list
        return photos_on_page
