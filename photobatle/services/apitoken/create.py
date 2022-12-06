from functools import lru_cache

from django import forms
from service_objects.services import ServiceWithResult
from rest_framework.authtoken.models import Token
from photobatle.models import User


class CreateAPITokenService(ServiceWithResult):
    """Service class for create user api token"""

    user_id = forms.IntegerField()

    def process(self):
        self.result = self._created_api_token
        return self

    @property
    def _created_api_token(self):
        if self._check_api_token:
            self._check_api_token.delete()
        return Token.objects.create(user=self._user)

    @property
    @lru_cache
    def _user(self):
        return User.objects.get(pk=self.cleaned_data['user_id'])

    @property
    @lru_cache()
    def _check_api_token(self):
        return Token.objects.filter(user=self._user)
