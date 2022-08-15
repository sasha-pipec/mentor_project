from django import forms
from django.db.models import Count
from service_objects.services import Service
from photobatle import models


class PersonalSortingFormService(Service):
    """Service class for personal sorting form"""

    form = forms.CharField()
    user_id = forms.IntegerField()

    @property
    def validate_form(self):
        sort_list = ['DEL', 'MOD', 'APR', 'REJ']
        if (self.cleaned_data['form'].split('=')[-1])[:3] in sort_list:
            return True
        raise Exception(f"Incorrect form value")

    def process(self):
        # We get the value of the form by which we will sort
        if self.validate_form:
            return models.Photomodels.Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                             like_count=Count('like_photo', distinct=True)).filter(
                moderation=(self.cleaned_data['form'].split('=')[-1])[:3], user_id=self.cleaned_data['user_id'])
