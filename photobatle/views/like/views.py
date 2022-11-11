from django.http import HttpResponse, JsonResponse
from django.views import View
from service_objects.services import ServiceOutcome

from photobatle.service import *


class CreatingLikeForPhoto(View):
    """Class for creating a like"""

    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                CreateLikeService, kwargs | {'user_id': request.user.id}
            )
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse({'button_text': 'Снять голос', 'like_count': str(outcome.result.like_count)},
                            status=status.HTTP_200_OK)


class DeletingLikeForPhoto(View):
    """Class for removing likes"""

    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                DeleteLikeService, kwargs | {'user_id': request.user.id}
            )
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse({'button_text': 'Лайк', 'like_count': str(outcome.result.like_count)},
                            status=status.HTTP_200_OK)
