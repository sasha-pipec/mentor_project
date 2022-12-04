from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from service_objects.services import ServiceOutcome

from api.constants import *
from api.custom_schema import *
from api.serializers import ApiCommentSerializer, ApiCreateCommentSerializer
from api.services import ListCommentForPhotoService, ApiCreateCommentService, ApiUpdateCommentService, \
    ApiDeleteCommentService
from api.utils import CustomTokenAuthentication


class CommentListCreateView(ListCreateAPIView):
    parser_classes = [MultiPartParser, ]
    authentication_classes = (CustomTokenAuthentication,)

    @swagger_auto_schema(responses={status.HTTP_200_OK: 'successes'})
    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                ListCommentForPhotoService, kwargs | {USER: request.user if request.user.is_authenticated else None}
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
                ApiCreateCommentService, request.POST.dict() | kwargs |
                                         {USER: request.user if request.user.is_authenticated else None}
            )
        except Exception as error:
            return Response(
                {
                    ERROR: {key: value for key, value in error.errors_dict.items()},
                    STATUS_ERROR: error.response_status
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(ApiCreateCommentSerializer(outcome.result, context={'request': request}).data,
                        outcome.response_status or status.HTTP_201_CREATED, )


class CommentUpdateDestroyView(APIView):
    parser_classes = [MultiPartParser, ]
    authentication_classes = (CustomTokenAuthentication,)

    @swagger_auto_schema(**COMMENT_DELETE)
    def delete(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                ApiDeleteCommentService, kwargs | {USER: request.user if request.user.is_authenticated else None}
            )
        except Exception as error:
            return Response(
                {
                    ERROR: {key: value for key, value in error.errors_dict.items()},
                    STATUS_ERROR: error.response_status
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(**COMMENT_PATCH)
    def patch(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                ApiUpdateCommentService, request.data.dict() | kwargs |
                                         {USER: request.user if request.user.is_authenticated else None}
            )
        except Exception as error:
            return Response(
                {
                    ERROR: {key: value for key, value in error.errors_dict.items()},
                    STATUS_ERROR: error.response_status
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(ApiCreateCommentSerializer(outcome.result, context={'request': request}).data,
                        outcome.response_status or status.HTTP_200_OK)
