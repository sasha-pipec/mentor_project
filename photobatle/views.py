from django.contrib.auth import logout
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from . import models
from . import forms
from . import serializers


# Create your views here.

def render_home_page(request):
    """Тут будет генерироваться главная  страничка приложения """
    form = forms.SortForm()
    posts = models.Photomodels.Photo.objects.filter(moderation='3')
    context = {
        'posts': posts,
        'form': form
    }
    return render(request, 'photobatle/home_html_with_post_and_SortForm.html', context=context)


def render_user_page(request):
    """Тут будет генерироваться личный кабинет пользователя """
    return render(request, 'photobatle/user_page.html')


def logout_user(request):
    """Выход из учетной записи"""
    logout(request)
    return redirect('home')


def sort_form_ajax(request):
    """Функция для AJAX запроса сортировка"""
    form = forms.SortForm()
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Получаем значение формы по которому будем сортировать
        field = request.POST['form'].split('=')[-1]
        serch_word = request.POST['name']
        posts = models.Photomodels.Photo.objects.filter(Q(user_name__username__icontains=serch_word) |
                                                        Q(photo_name__icontains=serch_word) |
                                                        Q(photo_content__icontains=serch_word),
                                                        moderation='3').order_by(f"-{field}")
        return JsonResponse({'posts': serializers.PhotoSerializer(posts, many=True).data}, status=200)
    return render(request, "home_html_with_post_and_SortForm.html", context={'form': form})


def serch_form_ajax(request):
    """Функция для AJAX запроса поиск по слову"""
    content = request.POST['name']
    posts = models.Photomodels.Photo.objects.filter(Q(user_name__username__icontains=content) |
                                                    Q(photo_name__icontains=content) |
                                                    Q(photo_content__icontains=content), moderation='3')
    return JsonResponse({'posts': serializers.PhotoSerializer(posts, many=True).data}, status=200)


def create_comment_for_photo(request):
    comment = request.POST['comment']
    photo_slug = request.POST['slug']
    user = request.user.id
    photo_id = models.Photomodels.Photo(pk=request.POST['pk'])
    models.Commentmodels.Comment.objects.create(photo=photo_id, user_name_id=user, content=comment)
    return redirect('detail_post', slug_id=photo_slug)


class DetailPost(DetailView):
    """Детальный просмотр поста"""
    model = models.Photomodels.Photo
    template_name = 'photobatle/detail_post.html'
    slug_url_kwarg = 'slug_id'
    context_object_name = 'post'

    def get_context_data(self,*args,oject_list=None, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['comments'] = models.Commentmodels.Comment.objects.filter(photo_id=context['post'].id)
        return context
