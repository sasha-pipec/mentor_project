from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from service_objects.services import ServiceOutcome

from api.serializers import ApiCommentSerializer
from api.service import *
from photobatle.serializers import *
from api.custom_schema import *
from photobatle.service import *


class CommentAPI(APIView):
    parser_classes = [MultiPartParser, ]

    @swagger_auto_schema(responses={status.HTTP_200_OK: 'successes'})
    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                GetCommentForPhotoService, kwargs | {'user_id': request.user.pk if request.user.pk else None}
            )
        except Exception as e:
            return Response({'error': str(e.detail), 'status_code': str(e.status_code)}, status=e.status_code)
        return Response(
            ApiCommentSerializer(outcome.result, context={'user_id': request.user.pk if request.user.pk else None},
                              many=True).data,
            outcome.response_status or status.HTTP_200_OK, )

    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=post_comment_parameters,
                         responses=post_comment_response, operation_description=post_comment_description)
    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                CreateCommentService, request.POST.dict() | kwargs | {'user_id': request.user.id}
            )
        except Exception as e:
            return Response({'error': str(e.detail), 'status_code': str(e.status_code)}, status=e.status_code)
        return Response(ApiCreateCommentSerializer(outcome.result).data,
                        outcome.response_status or status.HTTP_201_CREATED, )


class ModifiedCommentAPI(APIView):
    parser_classes = [MultiPartParser, ]

    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=delete_comment_parameters,
                         responses=delete_comment_response, operation_description=delete_comment_description)
    def delete(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                DeleteCommentService, kwargs | {'user_id': request.user.id}
            )
        except Exception as e:
            return Response({'error': str(e.detail), 'status_code': str(e.status_code)}, status=e.status_code)
        return Response({"message:": "comment deleted"}, status=status.HTTP_204_NO_CONTENT)

    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=patch_comment_parameters,
                         responses=patch_comment_response, operation_description=patch_comment_description)
    def patch(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                UpdateCommentService, request.data.dict() | kwargs | {'user_id': request.user.id}
            )
        except Exception as e:
            return Response({'error': str(e.detail), 'status_code': str(e.status_code)}, status=e.status_code)
        return Response(ApiCreateCommentSerializer(outcome.result).data,
                        outcome.response_status or status.HTTP_200_OK)
