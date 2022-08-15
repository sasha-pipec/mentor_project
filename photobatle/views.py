from django.views.generic import DetailView, ListView, TemplateView, View
from rest_framework.views import APIView
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse

from photobatle.service import *
from . import models
from . import forms
from . import serializers


# Create your views here.

def Logouting_user(request):
    """Log out of your account"""
    logout(request)
    return redirect('home')


class RenderingHomePage(ListView):
    """The main page of the application will be generated here"""
    model = models.Photomodels.Photo
    template_name = 'photobatle/home_html_with_post_and_SortForm.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.SortForm()
        return context

    def get_queryset(selfю, *, object_list=None, **kwargs):
        posts = super().get_queryset(**kwargs)
        return posts.filter(moderation='APR')


class RenderingUserPage(TemplateView):
    """The user's personal account will be generated here """
    template_name = 'photobatle/user_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_token'] = Token.objects.filter(user=self.request.user.id)
        return context


class CreatingCommentForPhoto(View):
    """Class for creating a comment"""

    def post(self, request, *args, **kwargs):
        try:
            CreateCommentService.execute(request.POST.dict() | kwargs | {'user_id': request.user.id})
        except Exception as error:
            return HttpResponse(error)
        return redirect('detail_post', slug_id=request.POST['photo_slug'])


class DeletingCommentForPhoto(View):
    """Class for deleting a comment"""

    def get(self, request, *args, **kwargs):
        try:
            photo_id = DeleteCommentService.execute(kwargs | {'user_id': request.user.id})
        except Exception as error:
            return HttpResponse(error)
        return redirect('detail_post', slug_id=photo_id.slug)


class UpdatingCommentForPhoto(View):
    """Class for changing the comment"""

    def post(self, request, *args, **kwargs):
        try:
            photo_id = UpdateCommentService.execute(request.POST.dict() | kwargs | {'user_id': request.user.id})
        except Exception as error:
            return HttpResponse(error)
        return redirect('detail_post', slug_id=photo_id.slug)


class CreatingLikeForPhoto(View):
    """Class for creating a like"""

    def get(self, request, *args, **kwargs):
        try:
            slug = CreateLikeService.execute(kwargs | {'user_id': request.user.id})
        except Exception as error:
            return HttpResponse(error)
        return redirect('detail_post', slug_id=slug)


class DeletingLikeForPhoto(View):
    """Class for removing likes"""

    def get(self, request, *args, **kwargs):
        try:
            slug = DeleteLikeService.execute(kwargs | {'user_id': request.user.id})
        except Exception as error:
            return HttpResponse(error)
        return redirect('detail_post', slug_id=slug)


class DetailPost(DataMixin, DetailView):
    """Detailed view of the post"""
    model = models.Photomodels.Photo
    template_name = 'photobatle/detail_post.html'
    slug_url_kwarg = 'slug_id'
    context_object_name = 'post'

    def get_context_data(self, parent_id=None, *args, oject_list=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # the main comments are stored here
        context['comments'] = models.Commentmodels.Comment.objects.filter(photo_id=context['post'].id,
                                                                          parent_id=parent_id)
        # answers to the main comments will be stored here
        context['answer_comments'] = []
        # we go through the main comments and look for their children
        for comment in context['comments']:
            context['answer_comments'] += [self.all_comments_for_post(parent_id=comment.pk, photo_id=comment.photo_id)]

        return context


class SortingFormAjax(APIView):
    """Class for AJAX request sorting"""

    def post(self, request, *args, **kwargs):
        # We get the value of the form by which we will sort
        try:
            posts = SortingFormService.execute(request.POST)
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse({'posts': serializers.PhotoSerializer(posts, many=True).data}, status=200)


class SearchFormAjax(APIView):
    """Class for AJAX query"""

    def post(self, request, *args, **kwargs):
        try:
            posts = SearchFormService.execute(request.POST)
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse({'posts': serializers.PhotoSerializer(posts, many=True).data}, status=200)


class PersonalSortingFormAjax(APIView):
    """Class for AJAX request sorting personal list posts"""

    def post(self, request, *args, **kwargs):
        try:
            posts = PersonalSortingFormService.execute(request.POST)
        except Exception as error:
            return HttpResponse(error)
        return JsonResponse({'posts': serializers.PhotoSerializer(posts, many=True).data}, status=200)


class AddPhoto(View):
    """Class for adding photos"""

    def get(self, *args, **kwargs):
        return render(self.request, 'photobatle/add_photo_form.html', context={'form': forms.AddPhotoForm()})

    def post(self, request, *args, **kwargs):
        try:
            AddPhotoService.execute(request.FILES.dict() | request.POST.dict() | {'user_id': request.user.id})
        except Exception as error:
            return HttpResponse(error)
        return redirect('home')


class UpdatePhoto(View):
    """Class for updating photos"""

    def post(self, request, *args, **kwargs):
        try:
            UpdatePhotoService.execute(
                request.FILES.dict() | request.POST.dict() | kwargs | {'user_id': request.user.id})
        except Exception as error:
            return HttpResponse(error)
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
    model = models.Photomodels.Photo
    template_name = 'photobatle/personal_list_posts.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.PersonalSortForm()
        context['change_form'] = forms.AddPhotoForm()
        return context

    def get_queryset(self, *, object_list=None, **kwargs):
        posts = super().get_queryset(**kwargs)
        return posts.filter(user_id=self.request.user)


class GeneratingAPIToken(View):
    def get(self, *args, **kwargs):
        try:
            CreateAPITokenService.execute(kwargs)
        except ValidationError as error:
            return HttpResponse(error)
        return redirect('user_page')
