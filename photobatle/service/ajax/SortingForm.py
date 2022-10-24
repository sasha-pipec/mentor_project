from django import forms
from django.core.paginator import Paginator
from django.db.models import Q, Count
from service_objects.services import Service
from photobatle.models import *


class SortingFormService(Service):
    """Service class for sorting form"""

    page = forms.CharField()
    sort_value = forms.CharField()
    search_value = forms.CharField(required=False)
    direction = forms.CharField(required=False)

    @property
    def validate_form(self):
        sort_list = ['like_count', 'comment_count', 'updated_at', 'id']
        if self.cleaned_data['sort_value'].split('=')[-1] not in sort_list:
            raise Exception(f"Incorrect sort_value")
        if self.cleaned_data['direction'] == 'asc':
            self.cleaned_data['sort_value'] = "-" + self.cleaned_data['sort_value'].split('=')[-1]
            return
        self.cleaned_data['sort_value'] = self.cleaned_data['sort_value'].split('=')[-1]

    def validate_page(self, page_range):
        if int(self.cleaned_data['page']) > page_range.stop:
            raise Exception(f"Incorrect page")

    def process(self):
        self.validate_form
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
