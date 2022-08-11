from rest_framework.response import Response
from rest_framework.views import APIView
from photobatle import serializers
from photobatle.service import *
from photobatle import models
from rest_framework import status


class HomePostListAPI(APIView):

    def get(self, *args, **kwargs):
        serializer = serializers.PhotoSerializer(
            models.Photomodels.Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                      like_count=Count('like_photo', distinct=True)).filter(
                moderation='APR'), many=True)
        return Response(serializer.data)


class CreatingCommentAPI(APIView):

    def post(self, request, *args, **kwargs):
        try:
            CreateCommentService.execute(request.data.dict() | {'user_id': request.user.id})
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=201)


class DeletingCommentAPI(APIView):

    def post(self, request, *args, **kwargs):
        try:
            DeleteCommentService.execute(kwargs | {'user_id': request.user.id})
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=201)

    # Create your views here.
