from django.urls import path, include
from . import views

urlpatterns = [
    # Классы предствавления
    path('', views.RenderingHomePage.as_view(), name='home'),
    path('user/', views.RenderingUserPage.as_view(), name='user_page'),

    path('photo/patch', views.AddPhoto.as_view(), name='create_photo'),
    path('photo/put/<slug:slug_id>', views.UpdatePhoto.as_view(), name='update_photo'),
    path('photo/delete/<slug:slug_id>', views.DeletePhoto.as_view(), name='delete_photo'),
    path('photo/recovery/<slug:slug_id>', views.RecoveryPhoto.as_view(), name='recovery_photo'),
    path('photo/get/personal_list_photo', views.PersonalListPosts.as_view(), name='personal_list_posts'),
    path('photo/get/<slug:slug_id>', views.DetailPost.as_view(), name='detail_post'),

    path('comment/patch/<parent_comment_id>', views.CreatingCommentForPhoto.as_view(), name='create_comment'),
    path('comment/delete/<comment_pk>', views.DeletingCommentForPhoto.as_view(), name='delete_comment'),
    path('comment/put/<comment_pk>', views.UpdatingCommentForPhoto.as_view(), name='update_comment'),

    path('like/patch/<photo_id>', views.CreatingLikeForPhoto.as_view(), name='create_like'),
    path('like/delete/<photo_id>', views.DeletingLikeForPhoto.as_view(), name='delete_like'),

    path('token/put/<user_id>', views.GeneratingAPIToken.as_view(), name='api_token'),

    # Функции предствавления
    path('logout_user/', views.Logouting_user, name='logout_user'),

    # AJAX запросы
    path('sort_form_ajax/', views.SortingFormAjax.as_view(), name='ajax'),
    path('serch_form_ajax/', views.SearchFormAjax.as_view(), name='ajax_second'),
    path('personal_sort_form_ajax/', views.PersonalSortingFormAjax.as_view(), name='personal_sort_form'),
]
