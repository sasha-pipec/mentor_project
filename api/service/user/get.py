from django import forms
from django.db.models import Value
from service_objects.services import ServiceWithResult
from photobatle.models import *
from api.status_code import *
from api.utils import *


class GetUserService(ServiceWithResult):
    """Service class for sorting form"""

    user_id = forms.IntegerField(required=False)

    custom_validations = ["validate_user_id"]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._get_user
        return self

    def validate_user_id(self):
        try:
            User.objects.get(pk=self.cleaned_data['user_id'])
        except Exception:
            if not self.cleaned_data['user_id']:
                raise ValidationError400(f'Missing one of all requirements parameters: api token')
            raise ValidationError404(f"Incorrect value of api token")

    @property
    def _get_user(self):
        return User.objects.get(pk=self.cleaned_data['user_id'])
