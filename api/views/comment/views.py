from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from service_objects.services import ServiceOutcome

from api.constants import *
from api.custom_schema import *
from api.serializers import ApiCommentSerializer, ApiCreateCommentSerializer
from api.services import GetCommentForPhotoService
from api.utils import CustomTokenAuthentication
from photobatle.services import CreateCommentService, DeleteCommentService, UpdateCommentService


class CommentListCreateView(ListCreateAPIView):
    parser_classes = [MultiPartParser, ]
    authentication_classes = (CustomTokenAuthentication,)

    @swagger_auto_schema(responses={status.HTTP_200_OK: 'successes'})
    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                GetCommentForPhotoService, kwargs | {ID_OF_USER: request.user.pk if request.user.pk else None}
            )
        except Exception as e:
            return Response({ERROR: e.detail, STATUS_ERROR: e.status_code}, status=e.status_code)
        return Response(
            ApiCommentSerializer(outcome.result, context={ID_OF_USER: request.user.pk if request.user.pk else None,
                                                          'request': request}, many=True).data,
            outcome.response_status or status.HTTP_200_OK, )

    @swagger_auto_schema(**COMMENT_CREATE)
    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                CreateCommentService, request.POST.dict() | kwargs | {ID_OF_USER: request.user.id}
            )
        except Exception as e:
            return Response({ERROR: e.detail, STATUS_ERROR: e.status_code}, status=e.status_code)
        return Response(ApiCreateCommentSerializer(outcome.result, context={'request': request}).data,
                        outcome.response_status or status.HTTP_201_CREATED, )


class CommentUpdateDestroyView(APIView):
    parser_classes = [MultiPartParser, ]
    authentication_classes = (CustomTokenAuthentication,)

    @swagger_auto_schema(**COMMENT_DELETE)
    def delete(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                DeleteCommentService, kwargs | {ID_OF_USER: request.user.id}
            )
        except Exception as e:
            return Response({ERROR: str(e.detail), STATUS_ERROR: str(e.status_code)}, status=e.status_code)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(**COMMENT_PATCH)
    def patch(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                UpdateCommentService, request.data.dict() | kwargs | {ID_OF_USER: request.user.id}
            )
        except Exception as e:
            return Response({ERROR: str(e.detail), STATUS_ERROR: str(e.status_code)}, status=e.status_code)
        return Response(ApiCreateCommentSerializer(outcome.result, context={'request': request}).data,
                        outcome.response_status or status.HTTP_200_OK)
