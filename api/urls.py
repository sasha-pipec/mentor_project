from django.urls import path
from .views import *

urlpatterns = [
    # User
    # Get method have 1 required params: api_token in headers
    path('user', UserRetrieve.as_view()),

    # Token
    path('token', TokenCreateView.as_view()),

    path('photos/personal', PersonalPhotoListView.as_view()),
    path('photos', PhotoListCreateView.as_view()),
    path('photos/<slug>', PhotoRetrieveUpdateDestroyView.as_view()),
    path('photos/<slug>/like_toggle', LikeCreateDestroyView.as_view()),
    path('photos/<slug>/comments', CommentListCreateView.as_view()),
    path('comments/<int:id>', CommentUpdateDestroyView.as_view()),

    # Personal photo
    # Get method have 1 required params: api_token in headers, not required: sort_value

    # Photo
    # Post method have 4 required params: photo, photo_name, photo_content, api_token in headers
    # Delete method have 2 required params: slug, api_token in headers
    # Patch method have 2 required params: slug, api_token in headers; not required photo, name, content
    # Get method have 1 required params: slug

    # Sort and search photo
    # Get method have 1 required params: form; 1 not required params name if you use sort photo
    # Get method have 1 required params: name if you use search photo

    # Personal sort photo
    # Get method have 2 required params: sort_value, api_token in headers

    # Comment
    # Post method have 3 required params:slug comment api_token in headers;
    # 2 not required params: parent_comment_id

    # Patch method have 3 required params: id,comment, api_token in headers
    # Delete method have 2 required params: id,comment, api_token in headers

    # Like
    # Post method have 2 required params: slug api_token in headers;
    # Delete method have 2 required params: slug api_token in headers;
]
