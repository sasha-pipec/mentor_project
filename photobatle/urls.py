from django.urls import path, include
from . import views

urlpatterns = [
    # Функции предствавления
    path('', views.render_home_page, name='home'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('user_page/', views.render_user_page, name='user_page'),
    path('create_comment_for_photo/', views.create_comment_for_photo, name='create_comment'),

    # Классы предствавления
    path('post/<slug:slug_id>', views.DetailPost.as_view(), name='detail_post'),

    # AJAX запросы
    path('sort_form_ajax/', views.sort_form_ajax, name='ajax'),
    path('serch_form_ajax/', views.serch_form_ajax, name='ajax_second'),
]
