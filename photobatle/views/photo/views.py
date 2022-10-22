from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from photobatle.forms import *
from photobatle.service import *
from photobatle.utils import DataMixin


class AddPhoto(View):
    """Class for adding photos"""

    def get(self, *args, **kwargs):
        return render(self.request, 'photobatle/add_photo_form.html', context={'form': AddPhotoForm()})

    def post(self, request, *args, **kwargs):
        try:
            AddPhotoService.execute(request.FILES.dict() | request.POST.dict() | {'user_id': request.user.id})
        except Exception as error:
            return render(request, 'photobatle/add_photo_form.html',
                          context={'form': AddPhotoForm(), 'error_message': error.message})
        return redirect('home')


class UpdatePhoto(View):
    """Class for updating photos"""

    def post(self, request, *args, **kwargs):
        try:
            UpdatePhotoService.execute(
                request.FILES.dict() | request.POST.dict() | kwargs | {'user_id': request.user.id})
        except Exception as error:
            return render(request, 'photobatle/personal_list_posts.html', context={'error_message': error.message})
        return redirect('personal_list_posts')


class DeletePhoto(View):
    """Class for deleting photos"""

    def get(self, request, *args, **kwargs):
        try:
            DeletePhotoService.execute(kwargs | {'user_id': request.user.id})
        except ValidationError as error:
            return HttpResponse(error)
        return redirect('personal_list_posts')


class RecoveryPhoto(View):
    """Class for recovery photos"""

    def get(self, *args, **kwargs):
        try:
            RecoveryPhotoService.execute(kwargs | {'user_id': self.request.user.id})
        except ValidationError as error:
            return HttpResponse(error)
        return redirect('personal_list_posts')


class PersonalListPosts(ListView):
    """A class for rendering the my photos personal page"""
    model = Photo
    template_name = 'photobatle/personal_list_posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PersonalSortForm()
        context['change_form'] = AddPhotoForm()
        return context

    def get_queryset(self, *, object_list=None, **kwargs):
        posts = super().get_queryset(**kwargs)
        return posts.filter(user_id=self.request.user)


class DetailPost(DataMixin, DetailView):
    """Detailed view of the post"""
    model = Photo
    template_name = 'photobatle/detail_post.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'

    def get_context_data(self, parent_id=None, *args, oject_list=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # the main comments are stored here
        context['comments'] = Comment.objects.filter(photo_id=context['post'].id,
                                                     parent_id=parent_id)
        # answers to the main comments will be stored here
        context['answer_comments'] = []
        # we go through the main comments and look for their children
        for comment in context['comments']:
            context['answer_comments'] += [self.all_comments_for_post(parent_id=comment.pk, photo_id=comment.photo_id)]

        return context
