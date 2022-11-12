from django import forms
from django.core.paginator import Paginator
from django.db.models import Count
from service_objects.services import ServiceWithResult
from photobatle.models import *
from api.status_code import *


class PersonalSortingFormService(ServiceWithResult):
    """Service class for personal sorting form"""

    sort_value = forms.CharField()
    user_id = forms.IntegerField(required=False)
    page = forms.CharField()

    custom_validations = ["validate_user_id", "validate_sort_value", ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._get_photo_on_page
        return self

    def validate_sort_value(self):
        sort_list = ['DEL', 'MOD', 'APR', 'REJ']
        if (self.cleaned_data['sort_value'].split('=')[-1])[:3] not in sort_list:
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
        all_photos = Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                            like_count=Count('like_photo', distinct=True)).filter(
            moderation=(self.cleaned_data['sort_value'].split('=')[-1])[:3], user_id=self.cleaned_data['user_id'])
        paginator = Paginator(all_photos, 4)
        self.validate_page(paginator.page_range)
        max_page = str(paginator.page_range[-1])
        photos_on_page = (paginator.page(int(self.cleaned_data['page']))).object_list
        return {'photos': photos_on_page, 'max_page': max_page}
