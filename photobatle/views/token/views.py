from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views import View

from photobatle.service import CreateAPITokenService


class GeneratingAPIToken(View):
    def get(self, *args, **kwargs):
        try:
            token = CreateAPITokenService.execute(kwargs)
        except ValidationError as error:
            return HttpResponse(error)
        return JsonResponse({'token': str(token)}, status=200)
