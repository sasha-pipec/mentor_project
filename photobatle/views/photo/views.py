from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from service_objects.services import ServiceOutcome

from photobatle.models import Photo, Comment
from photobatle.forms import AddPhotoForm, PersonalSortForm, SortForm
from photobatle.services import AddPhotoService, DeletePhotoService, UpdatePhotoService, RecoveryPhotoService
from photobatle.utils import DataMixin
from mentor_prooject.settings import REST_FRAMEWORK


class AddPhoto(View):
    """Class for adding photos"""

    def get(self, *args, **kwargs):
        return render(self.request, 'photobatle/add_photo_form.html', context={'form': AddPhotoForm()})

    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                AddPhotoService, request.POST.dict() | {'user': request.user}, request.FILES.dict()
            )
        except Exception as error:
            return render(request, 'photobatle/add_photo_form.html',
                          context={'form': AddPhotoForm(),
                                   'error_message': {key: value for key, value in error.errors_dict.items()}})
        return redirect('home')


class UpdatePhoto(View):
    """Class for updating photos"""

    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                UpdatePhotoService, request.POST.dict() | kwargs | {'user': request.user}, request.FILES.dict()
            )
        except Exception as error:
            return render(request, 'photobatle/personal_list_posts.html', context={'error_message': error})
        return redirect('personal_list_posts')


class DeletePhoto(View):
    """Class for deleting photos"""

    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                DeletePhotoService, kwargs | {'user': request.user}
            )
        except Exception as error:
            return HttpResponse(error)
        return redirect('personal_list_posts')


class RecoveryPhoto(View):
    """Class for recovery photos"""

    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                RecoveryPhotoService, kwargs | {'user': request.user}
            )
        except Exception as error:
            return HttpResponse(error)
        return redirect('personal_list_posts')


class PersonalListPosts(ListView):
    """A class for rendering the my photos personal page"""
    model = Photo
    template_name = 'photobatle/personal_list_posts.html'
    context_object_name = 'posts'
    paginate_by = REST_FRAMEWORK['PAGE_SIZE']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PersonalSortForm()
        context['change_form'] = AddPhotoForm()
        return context

    def get_queryset(self, *, object_list=None, **kwargs):
        posts = super().get_queryset(**kwargs)
        return posts.filter(user_id=self.request.user).order_by('id')


class RenderingHomePage(ListView):
    """The main page of the application will be generated here"""
    model = Photo
    template_name = 'photobatle/home_html_with_post_and_SortForm.html'
    context_object_name = 'posts'
    paginate_by = REST_FRAMEWORK['PAGE_SIZE']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SortForm()
        return context

    def get_queryset(self, *, object_list=None, **kwargs):
        posts = super().get_queryset(**kwargs)
        return posts.filter(moderation=Photo.APPROVED).order_by('id')


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
