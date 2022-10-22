from django import forms
from django.core.paginator import Paginator
from django.db.models import Count
from service_objects.services import Service
from photobatle.models import *


class PersonalSortingFormService(Service):
    """Service class for personal sorting form"""

    sort_value = forms.CharField()
    user_id = forms.IntegerField()
    page = forms.CharField()

    @property
    def validate_form(self):
        sort_list = ['DEL', 'MOD', 'APR', 'REJ']
        if (self.cleaned_data['sort_value'].split('=')[-1])[:3] not in sort_list:
            raise Exception(f"Incorrect sort_value")

    def validate_page(self, page_range):
        if int(self.cleaned_data['page']) > page_range.stop:
            raise Exception(f"Incorrect page")

    def process(self):
        # We get the value of the form by which we will sort
        self.validate_form
        all_photos = Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                            like_count=Count('like_photo', distinct=True)).filter(
            moderation=(self.cleaned_data['sort_value'].split('=')[-1])[:3], user_id=self.cleaned_data['user_id'])
        paginator = Paginator(all_photos, 2)
        self.validate_page(paginator.page_range)
        max_page = str(paginator.page_range[-1])
        photos_on_page = (paginator.page(int(self.cleaned_data['page']))).object_list
        return {'photos': photos_on_page, 'max_page': max_page}
