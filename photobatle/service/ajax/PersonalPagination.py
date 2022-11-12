from django import forms
from django.core.paginator import Paginator
from django.db.models import Count
from service_objects.services import ServiceWithResult
from photobatle.models import *
from api.status_code import *


class PersonalPaginationService(ServiceWithResult):
    """Service class for personal sorting form"""

    page = forms.CharField()
    user_id = forms.CharField(required=False)
    sort_value = forms.CharField(required=False)

    custom_validations = ["validate_user_id", "validate_sort_value", ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._get_photo_on_page
        return self

    def validate_sort_value(self):
        sort_list = ['DEL', 'MOD', 'APR', 'REJ']
        if self.cleaned_data['sort_value'] and self.cleaned_data['sort_value'] not in sort_list:
            raise ValidationError404(f"Incorrect sort_value")

    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"incorrect api token")

    def validate_page(self, page_range):
        try:
            if int(self.cleaned_data['page']) >= page_range.stop:
                raise ValidationError404(f"Incorrect page")
        except Exception:
            raise ValidationError404(f"Incorrect page")

    @property
    def _get_photo_on_page(self):
        if self.cleaned_data['sort_value']:
            all_photos = Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                like_count=Count('like_photo', distinct=True)).filter(
                user_id=self.cleaned_data['user_id'], moderation=self.cleaned_data['sort_value'])
        else:
            all_photos = Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                like_count=Count('like_photo', distinct=True)).filter(
                user_id=self.cleaned_data['user_id'])
        paginator = Paginator(all_photos, 4)
        self.validate_page(paginator.page_range)
        photos_on_page = (paginator.page(int(self.cleaned_data['page']))).object_list
        return photos_on_page
