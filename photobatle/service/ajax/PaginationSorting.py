from django import forms
from django.core.paginator import Paginator
from django.db.models import Count, Q
from service_objects.services import ServiceWithResult
from api.status_code import *
from photobatle.utils import *


class PaginationService(ServiceWithResult):
    """Service class for personal sorting form"""

    user_id = forms.CharField(required=False)
    sort_value = forms.CharField(required=False)
    search_value = forms.CharField(required=False)
    direction = forms.CharField(required=False)
    page = forms.CharField()

    def process(self):
        self.result = self._get_photo_on_page
        return self

    def validate_direction(self):
        if not self.cleaned_data['sort_value']:
            self.cleaned_data['sort_value'] = 'id'
        if self.cleaned_data['direction'] == 'desc':
            self.cleaned_data['sort_value'] = '-' + self.cleaned_data['sort_value']

    @property
    def _get_photo_on_page(self):
        if self.cleaned_data['user_id']:
            if self.cleaned_data['sort_value']:
                all_photos = Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                    like_count=Count('like_photo', distinct=True)).filter(
                    user_id=self.cleaned_data['user_id'], moderation=self.cleaned_data['sort_value'])
            else:
                all_photos = Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                    like_count=Count('like_photo', distinct=True)).filter(
                    user_id=self.cleaned_data['user_id'])
        else:
            self.validate_direction()
            all_photos = Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                like_count=Count('like_photo', distinct=True)).filter(
                Q(user__username__icontains=self.cleaned_data['search_value']) |
                Q(photo_name__icontains=self.cleaned_data['search_value']) |
                Q(photo_content__icontains=self.cleaned_data['search_value']),
                moderation='APR').order_by(self.cleaned_data['sort_value'])
        paginator = Paginator(all_photos, 4)
        photos_on_page = (paginator.page(int(self.cleaned_data['page']))).object_list
        max_page = str(paginator.page_range[-1])
        return {'photos': photos_on_page, 'max_page': max_page}
