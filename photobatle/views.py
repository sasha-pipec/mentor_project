from django.db.models import *
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, View, CreateView
from rest_framework.views import APIView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse

from . import models
from . import forms
from . import serializers


# Create your views here.

def Logouting_user(request):
    """Выход из учетной записи"""
    logout(request)
    return redirect('home')


class RenderingHomePage(ListView):
    """Тут будет генерироваться главная  страничка приложения """
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
    """Тут будет генерироваться личный кабинет пользователя """
    template_name = 'photobatle/user_page.html'


class CreatingCommentForPhoto(View):
    """Класс для создания комментария"""

    def post(self, *args, **kwargs):
        comment = self.request.POST['comment']
        photo_slug = self.request.POST['slug']
        user = self.request.user.id
        if len(comment) != 0:
            photo_id = models.Photomodels.Photo(pk=self.request.POST['pk'])
            if kwargs['parent_comment_id'] == 'none':
                # Создание записи комментария в бд
                models.Commentmodels.Comment.objects.create(photo=photo_id, user_name_id=user, content=comment)
            else:
                # Создание записи ответа на комментарий в бд
                models.Commentmodels.Comment.objects.create(photo=photo_id, user_name_id=user,
                                                            parent_id=kwargs['parent_comment_id'],
                                                            content=comment)
        return redirect('detail_post', slug_id=photo_slug)


class DeletingCommentForPhoto(View):
    """Класс для удаления комментария"""

    def get(self, *args, **kwargs):
        comment = models.Commentmodels.Comment.objects.get(pk=kwargs['comment_pk'])
        photo_slug = models.Photomodels.Photo.objects.get(pk=comment.photo_id)
        comment.delete()
        return redirect('detail_post', slug_id=photo_slug.slug)


class UpdatingCommentForPhoto(View):
    """Класс для изменения комментария"""

    def post(self, *args, **kwargs):
        comment_content = self.request.POST['comment']
        comment = models.Commentmodels.Comment.objects.get(pk=kwargs['comment_pk'])
        comment.content = comment_content
        comment.save()
        photo_slug = models.Photomodels.Photo.objects.get(pk=comment.photo_id)
        return redirect('detail_post', slug_id=photo_slug.slug)


class CreatingLikeForPhoto(View):
    """Класс для создания лайка"""

    def get(self, *args, **kwargs):
        photo = models.Photomodels.Photo.objects.get(pk=kwargs['photo_id'])
        user_id = self.request.user.id
        models.Likemodels.Like.objects.create(photo_id=kwargs['photo_id'], user_name_id=user_id)
        return redirect('detail_post', slug_id=photo.slug)


class DeletingLikeForPhoto(View):
    """Класс для удаления лайка"""

    def get(self, *args, **kwargs):
        photo = models.Photomodels.Photo.objects.get(pk=kwargs['photo_id'])
        user_id = self.request.user.id
        like = models.Likemodels.Like.objects.get(photo_id=kwargs['photo_id'], user_name_id=user_id)
        like.delete()
        return redirect('detail_post', slug_id=photo.slug)


class DetailPost(DetailView):
    """Детальный просмотр поста"""
    model = models.Photomodels.Photo
    template_name = 'photobatle/detail_post.html'
    slug_url_kwarg = 'slug_id'
    context_object_name = 'post'

    def all_comments_for_post(self, parent_id=None, photo_id=None):
        # функция для получения всех ответов под комментарием
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
        # тут хранятся основные комментарии
        context['comments'] = models.Commentmodels.Comment.objects.filter(photo_id=context['post'].id,
                                                                          parent_id=parent_id)
        # тут будут хранится ответы к основным комментариям
        context['answer_comments'] = []
        # перебираем основные комментарии и ищем их детей
        for comment in context['comments']:
            context['answer_comments'] += [self.all_comments_for_post(parent_id=comment.pk, photo_id=comment.photo_id)]

        return context


class SortingFormAjax(APIView):
    """Класс для AJAX запроса сортировка"""

    def post(self, *args, **kwargs):
        # Получаем значение формы по которому будем сортировать
        field = self.request.POST['form'].split('=')[-1]
        serch_word = self.request.POST['name']
        posts = models.Photomodels.Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                          like_count=Count('like_photo', distinct=True)).filter(
            Q(user_name__username__icontains=serch_word) |
            Q(photo_name__icontains=serch_word) |
            Q(photo_content__icontains=serch_word),
            moderation='3').order_by(f"-{field}")
        return JsonResponse({'posts': serializers.PhotoSerializer(posts, many=True).data}, status=200)


class SearchFormAjax(APIView):
    """Класс для AJAX запроса поиск по слову"""

    def post(self, *args, **kwargs):
        serch_word = self.request.POST['name']
        posts = models.Photomodels.Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                          like_count=Count('like_photo', distinct=True)).filter(
            Q(user_name__username__icontains=serch_word) |
            Q(photo_name__icontains=serch_word) |
            Q(photo_content__icontains=serch_word), moderation='3')
        return JsonResponse({'posts': serializers.PhotoSerializer(posts, many=True).data}, status=200)


class AddPhoto(CreateView):
    """Класс для добавления фотографии"""
    form_class = forms.AddPhotoForm
    template_name = 'photobatle/add_photo_form.html'
    success_url = reverse_lazy('home')
