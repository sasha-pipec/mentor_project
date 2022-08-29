from django.urls import path
from .consumers import *

ws_urlpatterns = [
    path('ws/test/', WSTest.as_asgi())
]
