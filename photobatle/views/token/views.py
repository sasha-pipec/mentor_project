from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View

from photobatle.service import CreateAPITokenService


class GeneratingAPIToken(View):
    def get(self, *args, **kwargs):
        try:
            CreateAPITokenService.execute(kwargs)
        except ValidationError as error:
            return HttpResponse(error)
        return redirect('user_page')
