from django.urls import path
from . import views

urlpatterns = [
    # Photo
    path('photo', views.PhotoAPI.as_view()),
    path('photo/<slug:slug_id>', views.ModifiedPhotoAPI.as_view()),

    # Comment
    path('comment', views.CommentAPI.as_view()),
    path('comment/<comment_pk>', views.ModifiedCommentAPI.as_view()),
]
