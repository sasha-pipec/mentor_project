from django.http import JsonResponse
from django.views.generic import ListView

from photobatle import serializers
from photobatle.forms import *
from photobatle.models import Photo


class RenderingHomePage(ListView):
    """The main page of the application will be generated here"""
    model = Photo
    template_name = 'photobatle/home_html_with_post_and_SortForm.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SortForm()
        return context

    def get_queryset(selfю, *, object_list=None, **kwargs):
        posts = super().get_queryset(**kwargs)
        return posts.filter(moderation='APR')
