from django.views.generic import TemplateView
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from django.shortcuts import redirect


class RenderingUserPage(TemplateView):
    """The user's personal account will be generated here """
    template_name = 'photobatle/user_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_token'] = Token.objects.filter(user=self.request.user.id)
        return context


def Logouting_user(request):
    """Log out of your account"""
    logout(request)
    return redirect('home')
