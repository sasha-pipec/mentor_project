from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from service_objects.services import ServiceOutcome

from api.custom_schema import *
from photobatle.service import *
from photobatle.serializers import *


class LikeAPI(APIView):
    parser_classes = [MultiPartParser, ]

    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=post_like_parameters,
                         responses=post_like_response, operation_description=post_like_description)
    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                CreateLikeService, request.data.dict() | {'user_id': request.user.id}
            )
        except Exception as e:
            return Response({'error': str(e.detail),
                             'status_code': str(e.status_code)}, status=e.status_code)
        return Response(PhotoSerializer(outcome.result).data,
                        outcome.response_status or status.HTTP_200_OK)


class ModifiedLikeAPI(APIView):
    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=delete_like_parameters,
                         responses=delete_like_response, operation_description=delete_like_description)
    def delete(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                DeleteLikeService, kwargs | {'user_id': request.user.id}
            )
        except Exception as e:
            return Response({'error': str(e.detail),
                             'status_code': str(e.status_code)}, status=e.status_code)
        return Response(PhotoSerializer(outcome.result).data,
                        outcome.response_status or status.HTTP_204_NO_CONTENT)
