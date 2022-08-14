from rest_framework.response import Response
from rest_framework.views import APIView
from photobatle import serializers
from photobatle.service import *
from photobatle import models
from rest_framework import status


class PhotoAPI(APIView):

    def get(self, *args, **kwargs):
        serializer = serializers.PhotoSerializer(
            models.Photomodels.Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                      like_count=Count('like_photo', distinct=True)).filter(
                moderation='APR'), many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            AddPhotoService.execute(request.FILES.dict() | request.POST.dict() | {'user_id': request.user.id})
        except Exception as error:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=201)


class ModifiedPhotoAPI(APIView):

    def delete(self, request, *args, **kwargs):
        try:
            DeleteCommentService.execute(kwargs | {'user_id': request.user.id})
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=204)

    def patch(self, request, *args, **kwargs):
        try:
            UpdateCommentService.execute(request.data.dict() | kwargs | {'user_id': request.user.id})
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=201)


class CommentAPI(APIView):

    def get(self, *args, **kwargs):
        serializer = serializers.CommentSerializer(
            models.Commentmodels.Comment.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            CreateCommentService.execute(request.data.dict() | {'user_id': request.user.id})
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=201)


class ModifiedCommentAPI(APIView):

    def delete(self, request, *args, **kwargs):
        try:
            DeleteCommentService.execute(kwargs | {'user_id': request.user.id})
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=204)

    def patch(self, request, *args, **kwargs):
        try:
            UpdateCommentService.execute(request.data.dict() | kwargs | {'user_id': request.user.id})
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=201)

    # Create your views here.
