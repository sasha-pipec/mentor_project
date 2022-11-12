from django.urls import path
from .views import *

urlpatterns = [
    # User
    # Get method have 1 required params: api_token in headers
    path('user', UserAPI.as_view()),

    # Photo
    # Post method have 4 required params: photo, photo_name, photo_content, api_token in headers
    # Delete method have 2 required params: slug_id, api_token in headers
    # Patch method have 2 required params: slug_id, api_token in headers; not required photo, photo_name, photo_content
    # Get method have 1 required params: slug_id
    path('photos', PhotoAPI.as_view()),
    path('pagination/page_range/', UserAPI.as_view()),
    path('personal_pagination/page_range/', UserAPI.as_view()),
    path('photos/<slug:slug>', ModifiedPhotoAPI.as_view()),

    path('photos/<slug:slug>/likes', LikeAPI.as_view()),
    path('photos/<slug:slug>/comments/<int:id>', LikeAPI.as_view()),

    # Personal photo
    # Get method have 1 required params: api_token in headers
    path('photos/personal/', PersonalSortPhotoApi.as_view()),

    # Sort and search photo
    # Get method have 1 required params: form; 1 not required params name if you use sort photo
    # Get method have 1 required params: name if you use search photo
    # path('photo/sort/', SortAndSearchPhotoApi.as_view()),

    # Personal sort photo
    # Get method have 2 required params: form, api_token in headers
    # path('photo/personal-sort/', PersonalSortPhotoApi.as_view()),

    # Comment
    # Post method have 3 required params:slug_id comment api_token in headers;
    # 2 not required params: parent_comment_id

    # Patch method have 3 required params: comment_pk,comment, api_token in headers
    # Delete method have 2 required params: comment_pk,comment, api_token in headers
    # path('comment', CommentAPI.as_view()),
    # path('comment/<comment_id>', ModifiedCommentAPI.as_view()),

    # Like
    # Post method have 2 required params: photo_id api_token in headers;
    # Delete method have 2 required params: photo_id api_token in headers;
    # path('like', LikeAPI.as_view()),
    # path('like/<photo_id>', ModifiedLikeAPI.as_view()),
]
