from django import forms
from django.db.models import Count
from service_objects.services import Service
from photobatle.models import *


class PersonalSortingFormService(Service):
    """Service class for personal sorting form"""

    sort_value = forms.CharField()
    user_id = forms.IntegerField()

    @property
    def validate_form(self):
        sort_list = ['DEL', 'MOD', 'APR', 'REJ']
        if (self.cleaned_data['sort_value'].split('=')[-1])[:3] in sort_list:
            return True
        raise Exception(f"Incorrect sort_value")

    def process(self):
        # We get the value of the form by which we will sort
        if self.validate_form:
            return Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                          like_count=Count('like_photo', distinct=True)).filter(
                moderation=(self.cleaned_data['sort_value'].split('=')[-1])[:3], user_id=self.cleaned_data['user_id'])
