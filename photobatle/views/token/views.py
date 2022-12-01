from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.views import View
from service_objects.services import ServiceOutcome

from photobatle.services import CreateAPITokenService


class GeneratingAPIToken(View):
    def get(self, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                CreateAPITokenService, kwargs
            )
        except ValidationError as error:
            return HttpResponse(error)
        return JsonResponse({
            'token': str(outcome.result)
        }, status=200)
