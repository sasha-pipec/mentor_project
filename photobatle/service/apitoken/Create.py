from functools import lru_cache

from django import forms
from service_objects.services import ServiceWithResult
from rest_framework.authtoken.models import Token
from api.status_code import *
from photobatle.models import User


class CreateAPITokenService(ServiceWithResult):
    """Service class for create user api token"""

    user_id = forms.IntegerField(required=False)

    custom_validations = ["validate_user_id", ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._created_api_token
        return self

    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"incorrect api token")

    @property
    @lru_cache()
    def _check_api_token(self):
        return Token.objects.filter(user=self.cleaned_data['user_id'])

    @property
    def _created_api_token(self):
        if self._check_api_token:
            self._check_api_token.delete()
        return Token.objects.create(user=User.objects.get(pk=self.cleaned_data['user_id']))
