from rest_framework.response import Response
from rest_framework.views import APIView
from photobatle import serializers
from photobatle.service import *
from photobatle import models


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
            CreateCommentService.execute(request.data)
        except Exception:
            return Response(status=404)
        return Response(status=201)

    # Create your views here.
