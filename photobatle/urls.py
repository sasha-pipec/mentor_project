from django.urls import path, include
from . import views

urlpatterns = [
    # Classes
    path('', views.RenderingHomePage.as_view(), name='home'),
    path('user/', views.RenderingUserPage.as_view(), name='user_page'),

    path('photo/post', views.AddPhoto.as_view(), name='create_photo'),
    path('photo/patch/<slug:slug>', views.UpdatePhoto.as_view(), name='update_photo'),
    path('photo/delete/<slug:slug>', views.DeletePhoto.as_view(), name='delete_photo'),
    path('photo/recovery/<slug:slug>', views.RecoveryPhoto.as_view(), name='recovery_photo'),
    path('photo/get/personal_list_photo', views.PersonalListPosts.as_view(), name='personal_list_posts'),
    path('photo/get/<slug:slug>', views.DetailPost.as_view(), name='detail_post'),

    path('comment/post/<parent_comment_id>', views.CreatingCommentForPhoto.as_view(), name='create_comment'),
    path('comment/delete/<comment_id>', views.DeletingCommentForPhoto.as_view(), name='delete_comment'),
    path('comment/patch/<comment_id>', views.UpdatingCommentForPhoto.as_view(), name='update_comment'),

    path('like/post/<photo_id>', views.CreatingLikeForPhoto.as_view(), name='create_like'),
    path('like/delete/<photo_id>', views.DeletingLikeForPhoto.as_view(), name='delete_like'),

    path('token/post/<user_id>', views.GeneratingAPIToken.as_view(), name='api_token'),

    # Function
    path('logout_user/', views.Logouting_user, name='logout_user'),

    # AJAX request
    path('sort_form_ajax/', views.SortingFormAjax.as_view(), name='ajax'),
    path('serch_form_ajax/', views.SearchFormAjax.as_view(), name='ajax_second'),
    path('personal_sort_form_ajax/', views.PersonalSortingFormAjax.as_view(), name='personal_sort_form'),
]
