from django import forms
from django.db.models import Q, Count
from service_objects.services import Service
from photobatle import models


class SearchFormService(Service):
    """Service class for search form"""

    name = forms.CharField()

    def process(self):
        name = self.cleaned_data['name']
        return models.Photomodels.Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                         like_count=Count('like_photo', distinct=True)).filter(
            Q(user__username__icontains=name) |
            Q(photo_name__icontains=name) |
            Q(photo_content__icontains=name), moderation='3')
