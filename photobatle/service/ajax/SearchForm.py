from django import forms
from django.core.paginator import Paginator
from django.db.models import Q, Count
from service_objects.services import ServiceWithResult
from photobatle.models import *
from api.status_code import *


class SearchFormService(ServiceWithResult):
    """Service class for search form"""

    search_value = forms.CharField(required=False)
    page = forms.CharField()

    def process(self):
        self.result = self._get_photo_on_page
        return self

    def validate_page(self, page_range):
        try:
            if int(self.cleaned_data['page']) >= page_range.stop:
                raise ValidationError404(f"Incorrect page")
        except Exception:
            raise ValidationError404(f"Incorrect page")

    @property
    def _get_photo_on_page(self):
        all_photos = Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                            like_count=Count('like_photo', distinct=True)).filter(
            Q(user__username__icontains=self.cleaned_data['search_value']) |
            Q(photo_name__icontains=self.cleaned_data['search_value']) |
            Q(photo_content__icontains=self.cleaned_data['search_value']),
            moderation='APR')
        paginator = Paginator(all_photos, 4)
        self.validate_page(paginator.page_range)
        max_page = str(paginator.page_range[-1])
        photos_on_page = (paginator.page(int(self.cleaned_data['page']))).object_list
        return {'photos': photos_on_page, 'max_page': max_page}
