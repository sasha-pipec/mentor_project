from django import forms
from service_objects.services import ServiceWithResult

from photobatle.models import *
from api.utils import *


class GetUserService(ServiceWithResult):
    """Api service class for get user"""

    user_id = forms.IntegerField(required=False)

    def process(self):
        self.result = self._get_user
        return self

    @property
    def _get_user(self):
        try:
            return User.objects.get(pk=self.cleaned_data['user_id'])
        except Exception:
            raise ValidationError401(f'Missing one of all requirements parameters: api token')