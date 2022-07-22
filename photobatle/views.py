from django.db.models import *
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import DetailView, ListView, TemplateView, View, CreateView
from rest_framework.views import APIView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse
from transliterate import translit

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
        return posts.filter(moderation='3')


class RenderingUserPage(TemplateView):
    """The user's personal account will be generated here """
    template_name = 'photobatle/user_page.html'


class CreatingCommentForPhoto(View):
    """Class for creating a comment"""

    def post(self, *args, **kwargs):
        comment = self.request.POST['comment']
        photo_slug = self.request.POST['slug']
        user = self.request.user.id
        if len(comment) != 0:
            photo_id = models.Photomodels.Photo(pk=self.request.POST['pk'])
            if kwargs['parent_comment_id'] == 'none':
                # Creating a comment entry in the database
                models.Commentmodels.Comment.objects.create(photo=photo_id, user_id=user, content=comment)
            else:
                # Creating a record of a response to a comment in the database
                models.Commentmodels.Comment.objects.create(photo=photo_id, user_id=user,
                                                            parent_id=kwargs['parent_comment_id'],
                                                            content=comment)
        return redirect('detail_post', slug_id=photo_slug)


class DeletingCommentForPhoto(View):
    """Class for deleting a comment"""

    def get(self, *args, **kwargs):
        comment = models.Commentmodels.Comment.objects.get(pk=kwargs['comment_pk'])
        photo_slug = models.Photomodels.Photo.objects.get(pk=comment.photo_id)
        comment.delete()
        return redirect('detail_post', slug_id=photo_slug.slug)


class UpdatingCommentForPhoto(View):
    """Class for changing the comment"""

    def post(self, *args, **kwargs):
        comment_content = self.request.POST['comment']
        comment = models.Commentmodels.Comment.objects.get(pk=kwargs['comment_pk'])
        comment.content = comment_content
        comment.save()
        photo_slug = models.Photomodels.Photo.objects.get(pk=comment.photo_id)
        return redirect('detail_post', slug_id=photo_slug.slug)


class CreatingLikeForPhoto(View):
    """Class for creating a like"""

    def get(self, *args, **kwargs):
        photo = models.Photomodels.Photo.objects.get(pk=kwargs['photo_id'])
        user_id = self.request.user.id
        models.Likemodels.Like.objects.create(photo_id=kwargs['photo_id'], user_id=user_id)
        return redirect('detail_post', slug_id=photo.slug)


class DeletingLikeForPhoto(View):
    """Class for removing likes"""

    def get(self, *args, **kwargs):
        photo = models.Photomodels.Photo.objects.get(pk=kwargs['photo_id'])
        user_id = self.request.user.id
        like = models.Likemodels.Like.objects.get(photo_id=kwargs['photo_id'], user_id=user_id)
        like.delete()
        return redirect('detail_post', slug_id=photo.slug)


class DetailPost(DetailView):
    """Detailed view of the post"""
    model = models.Photomodels.Photo
    template_name = 'photobatle/detail_post.html'
    slug_url_kwarg = 'slug_id'
    context_object_name = 'post'

    def all_comments_for_post(self, parent_id=None, photo_id=None):
        # function for getting all the answers under the comment
        comments = models.Commentmodels.Comment.objects.filter(photo_id=photo_id, parent_id=parent_id)
        all_answer_for_comment = []
        if len(comments) != 0:
            for comment in comments:
                all_answer_for_comment.append(comment)
                childs = self.all_comments_for_post(parent_id=comment.pk, photo_id=comment.photo_id, )
                if len(childs) != 0:
                    for child in childs:
                        all_answer_for_comment.append(child)
        else:
            return all_answer_for_comment
        return all_answer_for_comment

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

    def post(self, *args, **kwargs):
        # We get the value of the form by which we will sort
        field = self.request.POST['form'].split('=')[-1]
        query = self.request.POST['name']
        posts = models.Photomodels.Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                          like_count=Count('like_photo', distinct=True)).filter(
            Q(user__username__icontains=query) |
            Q(photo_name__icontains=query) |
            Q(photo_content__icontains=query),
            moderation='3').order_by(f"-{field}")
        return JsonResponse({'posts': serializers.PhotoSerializer(posts, many=True).data}, status=200)


class SearchFormAjax(APIView):
    """Class for AJAX query"""

    def post(self, *args, **kwargs):
        query = self.request.POST['name']
        posts = models.Photomodels.Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                          like_count=Count('like_photo', distinct=True)).filter(
            Q(user__username__icontains=query) |
            Q(photo_name__icontains=query) |
            Q(photo_content__icontains=query), moderation='3')
        return JsonResponse({'posts': serializers.PhotoSerializer(posts, many=True).data}, status=200)


class PersonalSortingFormAjax(APIView):
    """Class for AJAX request sorting personal list posts"""

    def post(self, *args, **kwargs):
        # We get the value of the form by which we will sort
        field = self.request.POST['form'].split('=')[-1]
        posts = models.Photomodels.Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                          like_count=Count('like_photo', distinct=True)).filter(
            moderation=field, user_id=self.request.user)
        return JsonResponse({'posts': serializers.PhotoSerializer(posts, many=True).data}, status=200)


class AddPhoto(CreateView):
    """Class for adding photos"""
    form_class = forms.AddPhotoForm
    template_name = 'photobatle/add_photo_form.html'
    success_url = reverse_lazy('home')

    def slug_russian_word(self, word):

        # Making a slug of Russian words
        russia = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        slug = ''
        for i in word:
            if i.lower() in russia:
                slug += translit(i, language_code='ru', reversed=True)
            else:
                if i == ' ':
                    slug += '-'
                else:
                    slug += i
        return slug

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.user_id = self.request.user.id
        fields.slug = self.slug_russian_word(self.request.POST['photo_name'])
        fields.save()
        return super().form_valid(form)


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


class UpdatePhoto(AddPhoto):
    """Class for updating photos"""

    def __init__(self):
        super().__init__()

    def post(self, *args, **kwargs):
        post = models.Photomodels.Photo.objects.get(slug=kwargs['slug_id'])
        if self.request.FILES.keys() & {'photo'}:
            post.photo = self.request.FILES['photo']
        post.slug = self.slug_russian_word(self.request.POST['photo_name'])
        post.photo_name = self.request.POST['photo_name']
        post.photo_content = self.request.POST['photo_content']
        post.save()
        return redirect('personal_list_posts')
