from django.contrib.auth import logout
from django.shortcuts import render, redirect


# Create your views here.

def render_home_page(request):
    """Тут будет генерироваться главная  страничка приложения """
    return render(request, 'photobatle/home_page.html')


def render_user_page(request):
    """Тут будет генерироваться личный кабинет пользователя """
    return render(request, 'photobatle/user_page.html')


def logout_user(request):
    """Выход из учетной записи"""
    logout(request)
    return redirect('home')
