from django import forms
from django.core.paginator import Paginator
from django.db.models import Q, Count
from service_objects.services import ServiceWithResult
from photobatle.models import *
from api.status_code import *


class SortingFormService(ServiceWithResult):
    """Service class for sorting form"""

    page = forms.CharField()
    sort_value = forms.CharField()
    search_value = forms.CharField(required=False)
    direction = forms.CharField(required=False)

    custom_validations = ["validate_sort_value", ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._get_photo_on_page
        return self

    def validate_sort_value(self):
        sort_list = ['like_count', 'comment_count', 'updated_at', 'id']
        if self.cleaned_data['sort_value'].split('=')[-1] not in sort_list:
            raise ValidationError400(f"Incorrect sort_value")
        if self.cleaned_data['direction'] == 'desc':
            self.cleaned_data['sort_value'] = "-" + self.cleaned_data['sort_value'].split('=')[-1]
            return
        self.cleaned_data['sort_value'] = self.cleaned_data['sort_value'].split('=')[-1]

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
        paginator = Paginator(all_photos, 4)
        self.validate_page(paginator.page_range)
        photos_on_page = (paginator.page(int(self.cleaned_data['page']))).object_list
        return photos_on_page
