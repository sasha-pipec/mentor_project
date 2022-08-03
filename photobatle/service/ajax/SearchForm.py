from django import forms
from django.db.models import Q, Count
from service_objects.services import Service
from photobatle import models


class SearchFormService(Service):
    """Service class for search form"""

    name = forms.CharField()

    def process(self):
        return models.Photomodels.Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                         like_count=Count('like_photo', distinct=True)).filter(
            Q(user__username__icontains=self.cleaned_data['name']) |
            Q(photo_name__icontains=self.cleaned_data['name']) |
            Q(photo_content__icontains=self.cleaned_data['name']), moderation='3')
