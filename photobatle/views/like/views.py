from django.http import HttpResponse, JsonResponse
from django.views import View

from photobatle.service import *


class CreatingLikeForPhoto(View):
    """Class for creating a like"""

    def get(self, request, *args, **kwargs):
        try:
            post=CreateLikeService.execute(kwargs | {'user_id': request.user.id})
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse({'button_text': 'Снять голос','like_count':str(post.like_count)}, status=200)


class DeletingLikeForPhoto(View):
    """Class for removing likes"""

    def get(self, request, *args, **kwargs):
        try:
            post=DeleteLikeService.execute(kwargs | {'user_id': request.user.id})
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse({'button_text': 'Лайк','like_count':str(post.like_count)}, status=200)
