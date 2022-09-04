from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from api.custom_schema import *
from photobatle.service import *


class LikeAPI(APIView):
    parser_classes = [MultiPartParser, ]

    @swagger_auto_schema(manual_parameters=post_like_parameters,
                         responses=post_like_response)
    def post(self, request, *args, **kwargs):
        try:
            CreateLikeService.execute(request.data.dict() | {'user_id': request.user.id})
        except Exception:
            return Response(status=status.HTTP_409_CONFLICT)
        return Response(status=201)


class ModifiedLikeAPI(APIView):

    @swagger_auto_schema(manual_parameters=delete_like_parameters,
                         responses=delete_like_response)
    def delete(self, request, *args, **kwargs):
        try:
            DeleteLikeService.execute(kwargs | {'user_id': request.user.id})
        except Exception:
            return Response(status=status.HTTP_409_CONFLICT)
        return Response(status=204)
