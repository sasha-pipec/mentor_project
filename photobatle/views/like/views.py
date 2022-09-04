from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View

from photobatle.service import *


class CreatingLikeForPhoto(View):
    """Class for creating a like"""

    def get(self, request, *args, **kwargs):
        try:
            slug = CreateLikeService.execute(kwargs | {'user_id': request.user.id})
        except Exception as error:
            return HttpResponse(error)
        return redirect('detail_post', slug=slug)


class DeletingLikeForPhoto(View):
    """Class for removing likes"""

    def get(self, request, *args, **kwargs):
        try:
            slug = DeleteLikeService.execute(kwargs | {'user_id': request.user.id})
        except Exception as error:
            return HttpResponse(error)
        return redirect('detail_post', slug=slug)
