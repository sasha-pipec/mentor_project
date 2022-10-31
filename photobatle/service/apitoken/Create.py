from django import forms
from service_objects.services import Service
from rest_framework.authtoken.models import Token
from api.status_code import *
from photobatle.models import User


class CreateAPITokenService(Service):
    """Service class for create user api token"""

    user_id = forms.IntegerField(required=False)

    def process(self):
        self.validate_user_id
        if Token.objects.filter(user=self.cleaned_data['user_id']):
            Token.objects.filter(user=self.cleaned_data['user_id']).delete()
        return Token.objects.create(user=User.objects.get(pk=self.cleaned_data['user_id']))

    @property
    def validate_user_id(self):
        if not self.cleaned_data['user_id']:
            raise ValidationError401(f"incorrect api token")
