from django import forms
from django.core.paginator import Paginator
from django.db.models import Count, Q
from service_objects.services import ServiceWithResult

from photobatle.utils import *
from mentor_prooject.settings import REST_FRAMEWORK


class PaginationService(ServiceWithResult):
    """Service class for personal sorting form"""

    user_id = forms.IntegerField(required=False)
    sort_value = forms.CharField(required=False)
    search_value = forms.CharField(required=False)
    direction = forms.CharField(required=False)
    page = forms.IntegerField()

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
        photos_on_page = Paginator(all_photos, REST_FRAMEWORK['PAGE_SIZE']).page(self.cleaned_data['page'])
        max_page = photos_on_page.paginator.page_range.stop
        return {'photos': photos_on_page, 'max_page': max_page-1}
