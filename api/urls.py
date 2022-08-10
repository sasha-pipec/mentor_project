from django.urls import path
from . import views

urlpatterns = [
    path('api/home', views.HomePostListAPI.as_view()),

    path('api/comment/patch', views.CreatingCommentAPI.as_view())
]
