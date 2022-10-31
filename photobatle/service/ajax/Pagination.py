from django import forms
from django.core.paginator import Paginator
from django.db.models import Count, Q
from service_objects.services import Service
from photobatle.models import *
from api.status_code import *


class PaginationService(Service):
    """Service class for personal sorting form"""

    sort_value = forms.CharField(required=False)
    search_value = forms.CharField(required=False)
    direction = forms.CharField()
    page = forms.CharField()

    def process(self):
        self.validate_sort_value
        self.validate_direction
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

    @property
    def validate_sort_value(self):
        sort_list = ['like_count', 'comment_count', 'updated_at', 'id']
        if not self.cleaned_data['sort_value']:
            self.cleaned_data['sort_value'] = 'id'
        if self.cleaned_data['sort_value'] not in sort_list:
            raise ValidationError400(f"Incorrect sort_value")

    @property
    def validate_direction(self):
        if self.cleaned_data['direction'] == 'desc':
            self.cleaned_data['sort_value'] = '-' + self.cleaned_data['sort_value']

    def validate_page(self, page_range):
        if int(self.cleaned_data['page']) > page_range.stop:
            raise ValidationError400(f"Incorrect page")
