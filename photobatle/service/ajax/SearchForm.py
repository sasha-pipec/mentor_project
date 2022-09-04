from django import forms
from django.db.models import Q, Count
from service_objects.services import Service
from photobatle.models import *


class SearchFormService(Service):
    """Service class for search form"""

    search_value = forms.CharField()

    def process(self):
        return Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                      like_count=Count('like_photo', distinct=True)).filter(
            Q(user__username__icontains=self.cleaned_data['search_value']) |
            Q(photo_name__icontains=self.cleaned_data['search_value']) |
            Q(photo_content__icontains=self.cleaned_data['search_value']), moderation='APR')
