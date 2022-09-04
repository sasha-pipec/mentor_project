from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View

from photobatle.service import *


class CreatingCommentForPhoto(View):
    """Class for creating a comment"""

    def post(self, request, *args, **kwargs):
        try:
            CreateCommentService.execute(request.POST.dict() | kwargs | {'user_id': request.user.id})
        except Exception as error:
            return HttpResponse(error)
        return redirect('detail_post', slug=request.POST['photo_slug'])


class DeletingCommentForPhoto(View):
    """Class for deleting a comment"""

    def get(self, request, *args, **kwargs):
        try:
            photo_id = DeleteCommentService.execute(kwargs | {'user_id': request.user.id})
        except Exception as error:
            return HttpResponse(error)
        return redirect('detail_post', slug=photo_id.slug)


class UpdatingCommentForPhoto(View):
    """Class for changing the comment"""

    def post(self, request, *args, **kwargs):
        try:
            photo_id = UpdateCommentService.execute(request.POST.dict() | kwargs | {'user_id': request.user.id})
        except Exception as error:
            return HttpResponse(error)
        return redirect('detail_post', slug=photo_id.slug)
