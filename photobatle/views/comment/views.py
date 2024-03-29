from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from service_objects.services import ServiceOutcome

from photobatle.services import CreateCommentService, DeleteCommentService, UpdateCommentService


class CreatingCommentForPhoto(View):
    """Class for creating a comment"""

    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                CreateCommentService, request.POST.dict() | kwargs | {'user': request.user}
            )
        except Exception as error:
            return HttpResponse(error)
        return redirect('detail_post', slug=request.POST['slug'])


class DeletingCommentForPhoto(View):
    """Class for deleting a comment"""

    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                DeleteCommentService, kwargs | {'user': request.user}
            )
        except Exception as error:
            return HttpResponse(error)
        return redirect('detail_post', slug=outcome.result.slug)


class UpdatingCommentForPhoto(View):
    """Class for changing the comment"""

    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                UpdateCommentService, request.POST.dict() | kwargs | {'user': request.user}
            )
        except Exception as error:
            return HttpResponse(error)
        return redirect('detail_post', slug=outcome.service.cleaned_data['slug'])
