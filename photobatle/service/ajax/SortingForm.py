from django import forms
from django.db.models import Q, Count
from service_objects.services import Service
from photobatle import models


class SortingFormService(Service):
    """Service class for sorting form"""

    form = forms.CharField()
    name = forms.CharField(required=False)

    @property
    def validate_form(self):
        sort_list = ['like_count', 'comment_count', 'updated_at']
        if self.cleaned_data['form'].split('=')[-1] in sort_list:
            return True
        raise Exception(f"Incorrect form value")

    def process(self):
        if self.validate_form:
            return models.Photomodels.Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                             like_count=Count('like_photo', distinct=True)).filter(
                Q(user__username__icontains=self.cleaned_data['name']) |
                Q(photo_name__icontains=self.cleaned_data['name']) |
                Q(photo_content__icontains=self.cleaned_data['name']),
                moderation='APR').order_by(f"-{self.cleaned_data['form'].split('=')[-1]}")
