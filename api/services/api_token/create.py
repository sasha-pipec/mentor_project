from functools import lru_cache

from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from rest_framework.authtoken.models import Token
from api.status_code import ValidationError401
from photobatle.models import User


class ApiCreateApiTokenService(ServiceWithResult):
    """Service class for create user api token"""

    user = ModelField(User, required=False)

    custom_validations = ["check_user_presence", ]

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._created_api_token
        return self

    @property
    def _created_api_token(self):
        if self._check_api_token:
            self._check_api_token.first().delete()
        return Token.objects.create(user=self.cleaned_data['user'])

    def check_user_presence(self):
        if not self.cleaned_data['user']:
            raise ValidationError401("Missing required parameter: api token")

    @property
    @lru_cache()
    def _check_api_token(self):
        return Token.objects.filter(user=self.cleaned_data['user'])
