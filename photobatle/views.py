from django.db.models import *
from django.views.generic import DetailView
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import JsonResponse

from . import models
from . import forms
from . import serializers


# Create your views here.

def Rendering_home_page(request):
    """Тут будет генерироваться главная  страничка приложения """
    form = forms.SortForm()
    posts = models.Photomodels.Photo.objects.filter(moderation='3')
    context = {
        'posts': posts,
        'form': form
    }
    return render(request, 'photobatle/home_html_with_post_and_SortForm.html', context=context)


def Rendering_user_page(request):
    """Тут будет генерироваться личный кабинет пользователя """
    return render(request, 'photobatle/user_page.html')


def Logouting_user(request):
    """Выход из учетной записи"""
    logout(request)
    return redirect('home')


def Creating_comment_for_photo(request, parent_comment_id):
    """Функция создания комментария для поста"""
    comment = request.POST['comment']
    photo_slug = request.POST['slug']
    user = request.user.id
    if len(comment) != 0:
        photo_id = models.Photomodels.Photo(pk=request.POST['pk'])
        if parent_comment_id == 'none':
            # Создание записи комментария в бд
            models.Commentmodels.Comment.objects.create(photo=photo_id, user_name_id=user, content=comment)
        else:
            # Создание записи ответа на комментарий в бд
            models.Commentmodels.Comment.objects.create(photo=photo_id, user_name_id=user, parent_id=parent_comment_id,
                                                        content=comment)
    return redirect('detail_post', slug_id=photo_slug)


def Deleting_comment_for_photo(request, comment_pk):
    """Функция для удаления комментария"""
    comment = models.Commentmodels.Comment.objects.get(pk=comment_pk)
    photo_slug = models.Photomodels.Photo.objects.get(pk=comment.photo_id)
    comment.delete()
    return redirect('detail_post', slug_id=photo_slug.slug)


def Updating_comment_for_photo(request, comment_pk):
    """Функция для изменения комментария"""
    comment_content = request.POST['comment']
    comment = models.Commentmodels.Comment.objects.get(pk=comment_pk)
    comment.content = comment_content
    comment.save()
    photo_slug = models.Photomodels.Photo.objects.get(pk=comment.photo_id)
    return redirect('detail_post', slug_id=photo_slug.slug)


def Creating_like_for_photo(request, photo_id):
    """Функция для создания лайка"""
    photo = models.Photomodels.Photo.objects.get(pk=photo_id)
    user_id = request.user.id
    models.Likemodels.Like.objects.create(photo_id=photo_id, user_name_id=user_id)
    return redirect('detail_post', slug_id=photo.slug)


def Deleting_like_for_photo(request, photo_id):
    """Функция для удаления лайка"""
    photo = models.Photomodels.Photo.objects.get(pk=photo_id)
    user_id = request.user.id
    like = models.Likemodels.Like.objects.get(photo_id=photo_id, user_name_id=user_id)
    like.delete()
    return redirect('detail_post', slug_id=photo.slug)


def Sorting_form_ajax(request):
    """Функция для AJAX запроса сортировка"""
    form = forms.SortForm()
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Получаем значение формы по которому будем сортировать
        field = request.POST['form'].split('=')[-1]
        serch_word = request.POST['name']
        posts = models.Photomodels.Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                          like_count=Count('like_photo', distinct=True)).filter(
            Q(user_name__username__icontains=serch_word) |
            Q(photo_name__icontains=serch_word) |
            Q(photo_content__icontains=serch_word),
            moderation='3').order_by(f"-{field}")
        let = vars(posts[0])
        return JsonResponse({'posts': serializers.PhotoSerializer(posts, many=True).data}, status=200)
    return render(request, "home_html_with_post_and_SortForm.html", context={'form': form})


def Search_form_ajax(request):
    """Функция для AJAX запроса поиск по слову"""
    serch_word = request.POST['name']
    posts = models.Photomodels.Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                      like_count=Count('like_photo', distinct=True)).filter(
        Q(user_name__username__icontains=serch_word) |
        Q(photo_name__icontains=serch_word) |
        Q(photo_content__icontains=serch_word), moderation='3')
    return JsonResponse({'posts': serializers.PhotoSerializer(posts, many=True).data}, status=200)


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
