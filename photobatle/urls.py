from django.urls import path, include
from .views import *

urlpatterns = [
    # Classes
    path('', RenderingHomePage.as_view(), name='home'),
    path('user/', RenderingUserPage.as_view(), name='user_page'),

    path('photo/post', AddPhoto.as_view(), name='create_photo'),
    path('photo/patch/<slug:slug>', UpdatePhoto.as_view(), name='update_photo'),
    path('photo/delete/<slug:slug>', DeletePhoto.as_view(), name='delete_photo'),
    path('photo/recovery/<slug:slug>', RecoveryPhoto.as_view(), name='recovery_photo'),
    path('photo/get/personal_list_photo', PersonalListPosts.as_view(), name='personal_list_posts'),
    path('photo/get/<slug:slug>', DetailPost.as_view(), name='detail_post'),

    path('comment/post/<parent_comment_id>', CreatingCommentForPhoto.as_view(), name='create_comment'),
    path('comment/delete/<comment_id>', DeletingCommentForPhoto.as_view(), name='delete_comment'),
    path('comment/patch/<comment_id>', UpdatingCommentForPhoto.as_view(), name='update_comment'),

    path('like/post/<photo_id>', CreatingLikeForPhoto.as_view(), name='create_like'),
    path('like/delete/<photo_id>', DeletingLikeForPhoto.as_view(), name='delete_like'),

    path('token/post/<user_id>', GeneratingAPIToken.as_view(), name='api_token'),

    # Function
    path('logout_user/', Logouting_user, name='logout_user'),

    # AJAX request
    path('sort_form_ajax/', SortingFormAjax.as_view(), name='ajax'),
    path('serch_form_ajax/', SearchFormAjax.as_view(), name='ajax_second'),
    path('personal_sort_form_ajax/', PersonalSortingFormAjax.as_view(), name='personal_sort_form'),
]
