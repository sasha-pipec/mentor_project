from django import forms
from django.core.paginator import Paginator
from django.db.models import Count
from service_objects.services import Service
from photobatle.models import *


class PersonalPaginationService(Service):
    """Service class for personal sorting form"""

    page = forms.CharField()
    user_id = forms.CharField()
    sort_value = forms.CharField(required=False)

    @property
    def validate_sort_value(self):
        sort_list = ['DEL', 'MOD', 'APR', 'REJ']
        if self.cleaned_data['sort_value'] not in sort_list:
            raise Exception(f"Incorrect sort_value")

    def validate_page(self, page_range):
        if int(self.cleaned_data['page']) > page_range.stop:
            raise Exception(f"Incorrect page")

    def process(self):
        if self.cleaned_data['sort_value']:
            self.validate_sort_value
            all_photos = Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                like_count=Count('like_photo', distinct=True)).filter(
                user_id=self.cleaned_data['user_id'], moderation=self.cleaned_data['sort_value'])
        else:
            all_photos = Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                like_count=Count('like_photo', distinct=True)).filter(
                user_id=self.cleaned_data['user_id'])
        paginator = Paginator(all_photos, 2)
        self.validate_page(paginator.page_range)
        photos_on_page = (paginator.page(int(self.cleaned_data['page']))).object_list
        return photos_on_page