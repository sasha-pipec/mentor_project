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


def Creating_comment_for_photo(request):
    """Функция создания комментария для поста"""
    comment = request.POST['comment']
    photo_slug = request.POST['slug']
    user = request.user.id
    if len(comment) != 0:
        # Создание записи комментария в бд
        photo_id = models.Photomodels.Photo(pk=request.POST['pk'])
        models.Commentmodels.Comment.objects.create(photo=photo_id, user_name_id=user, content=comment)
    return redirect('detail_post', slug_id=photo_slug)


def Sorting_form_ajax(request):
    """Функция для AJAX запроса сортировка"""
    form = forms.SortForm()
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Получаем значение формы по которому будем сортировать
        field = request.POST['form'].split('=')[-1]
        serch_word = request.POST['name']
        posts = models.Photomodels.Photo.objects.annotate(comment_count=Count('comment_photo')).filter(Q(user_name__username__icontains=serch_word) |
                                                        Q(photo_name__icontains=serch_word) |
                                                        Q(photo_content__icontains=serch_word),
                                                        moderation='3').order_by(f"-{field}")
        return JsonResponse({'posts': serializers.PhotoSerializer(posts, many=True).data}, status=200)
    return render(request, "home_html_with_post_and_SortForm.html", context={'form': form})


def Search_form_ajax(request):
    """Функция для AJAX запроса поиск по слову"""
    serch_word = request.POST['name']
    posts = models.Photomodels.Photo.objects.annotate(comment_count=Count('comment_photo')).filter(Q(user_name__username__icontains=serch_word) |
                                                    Q(photo_name__icontains=serch_word) |
                                                    Q(photo_content__icontains=serch_word), moderation='3')
    return JsonResponse({'posts': serializers.PhotoSerializer(posts, many=True).data}, status=200)


class DetailPost(DetailView):
    """Детальный просмотр поста"""
    model = models.Photomodels.Photo
    template_name = 'photobatle/detail_post.html'
    slug_url_kwarg = 'slug_id'
    context_object_name = 'post'

    def get_context_data(self, *args, oject_list=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['comments'] = models.Commentmodels.Comment.objects.filter(photo_id=context['post'].id)
        return context
