from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from service_objects.services import ServiceOutcome

from api.custom_schema import *
from api.service import ApiCreateLikeService, ApiDeleteLikeService
from api.constants import *
from api.utils import _like_exist


class LikeAPI(APIView):
    parser_classes = [MultiPartParser, ]

    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=post_like_parameters,
                         responses=post_like_response, operation_description=post_like_description)
    def post(self, request, *args, **kwargs):
        try:
            if _like_exist(request.user.id, kwargs['slug']):
                outcome = ServiceOutcome(
                    ApiCreateLikeService, kwargs | {ID_OF_USER: request.user.id}
                )
            else:
                outcome = ServiceOutcome(
                    ApiDeleteLikeService, kwargs | {ID_OF_USER: request.user.id}
                )
        except Exception as e:
            return Response({ERROR: e.detail, STATUS_ERROR: e.status_code}, status=e.status_code)
        return Response({RESPONSE: {'is_liked_by_current_user': outcome.result}},
                        status=outcome.response_status)
