from django.urls import path, include
from . import views

urlpatterns = [
    # Классы предствавления
    path('', views.RenderingHomePage.as_view(), name='home'),
    path('User/', views.RenderingUserPage.as_view(), name='user_page'),
    path('Photo/get/<slug:slug_id>', views.DetailPost.as_view(), name='detail_post'),
    path('Comment/patch/<parent_comment_id>', views.CreatingCommentForPhoto.as_view(), name='create_comment'),
    path('Comment/delete/<comment_pk>', views.DeletingCommentForPhoto.as_view(), name='delete_comment'),
    path('Comment/put/<comment_pk>', views.UpdatingCommentForPhoto.as_view(), name='update_comment'),

    path('Like/patch/<photo_id>', views.CreatingLikeForPhoto.as_view(), name='create_like'),
    path('Like/delete/<photo_id>', views.DeletingLikeForPhoto.as_view(), name='delete_like'),

    # Функции предствавления
    path('logout_user/', views.Logouting_user, name='logout_user'),

    # AJAX запросы
    path('sort_form_ajax/', views.SortingFormAjax.as_view(), name='ajax'),
    path('serch_form_ajax/', views.SearchFormAjax.as_view(), name='ajax_second'),
]
