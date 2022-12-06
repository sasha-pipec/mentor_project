from django import forms
from django.core.paginator import Paginator
from django.db.models import Count, Q
from service_objects.services import ServiceWithResult

from mentor_prooject.settings import REST_FRAMEWORK
from photobatle.models import Photo


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
        all_photos = Photo.objects.all().order_by('id')
        if self.cleaned_data['user_id']:
            all_photos = all_photos.filter(user_id=int(self.cleaned_data['user_id']))
            if self.cleaned_data['sort_value']:
                all_photos = all_photos.filter(moderation=self.cleaned_data['sort_value'])
        else:
            self.validate_direction()
            all_photos = all_photos.filter(moderation=Photo.APPROVED).order_by(self.cleaned_data['sort_value'])
            if self.cleaned_data['search_value']:
                all_photos = all_photos.filter(
                    Q(user__username__icontains=self.cleaned_data['search_value']) |
                    Q(photo_name__icontains=self.cleaned_data['search_value']) |
                    Q(photo_content__icontains=self.cleaned_data['search_value']),
                )
        photos_on_page = Paginator(all_photos, REST_FRAMEWORK['PAGE_SIZE']).page(int(self.cleaned_data['page']))
        return photos_on_page
