from django.urls import path
from . import views

urlpatterns = [
    # User
    # Get method have 1 required params: api_token in headers
    path('user', views.UserAPI.as_view()),

    # Photo
    # Post method have 4 required params: photo, photo_name, photo_content, api_token in headers
    # Delete method have 2 required params: slug_id, api_token in headers
    # Patch method have 2 required params: slug_id, api_token in headers; not required photo, photo_name, photo_content
    # Get method have 1 required params: slug_id
    path('photo', views.PhotoAPI.as_view()),
    path('photo/<slug:slug_id>', views.ModifiedPhotoAPI.as_view()),

    # Personal photo
    # Get method have 1 required params: api_token in headers
    path('photo/personal/', views.PersonalPhotoAPI.as_view()),

    # Sort and search photo
    # Get method have 1 required params: form; 1 not required params name if you use sort photo
    # Get method have 1 required params: name if you use search photo
    path('photo/sort/', views.SortAndSearchPhotoApi.as_view()),

    # Personal sort photo
    # Get method have 2 required params: form, api_token in headers
    path('photo/personal-sort/', views.PersonalSortPhotoApi.as_view()),

    # Comment
    # Post method have 3 required params:slug_id comment api_token in headers;
    # 2 not required params: parent_comment_id

    # Patch method have 3 required params: comment_pk,comment, api_token in headers
    # Delete method have 2 required params: comment_pk,comment, api_token in headers
    path('comment', views.CommentAPI.as_view()),
    path('comment/<comment_pk>', views.ModifiedCommentAPI.as_view()),

    # Like
    # Post method have 2 required params: photo_id api_token in headers;
    # Delete method have 2 required params: photo_id api_token in headers;
    path('like', views.LikeAPI.as_view()),
    path('like/<photo_id>', views.ModifiedLikeAPI.as_view()),
]
