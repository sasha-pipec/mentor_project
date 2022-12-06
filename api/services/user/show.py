from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField

from api.status_code import ValidationError401
from photobatle.models import User


class GetUserService(ServiceWithResult):
    """Api service class for get user"""

    user = ModelField(User, required=False)

    def process(self):
        self.result = self._get_user
        return self

    @property
    def _get_user(self):
        if self.cleaned_data['user']:
            return self.cleaned_data['user']
        raise ValidationError401(f'Missing one of all requirements parameters: api token')
