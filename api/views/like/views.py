from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from service_objects.services import ServiceOutcome

from api.custom_schema import LIKE_TOGGLE
from api.services import ApiLikeToggleService
from api.constants import *
from api.utils import CustomTokenAuthentication


class LikeCreateDestroyView(APIView):
    parser_classes = [MultiPartParser, ]
    authentication_classes = (CustomTokenAuthentication,)

    @swagger_auto_schema(**LIKE_TOGGLE)
    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                ApiLikeToggleService, kwargs | {USER: request.user if request.user.is_authenticated else None}
            )
        except Exception as error:
            return Response(
                {
                    ERROR: {key: value for key, value in error.errors_dict.items()},
                    STATUS_ERROR: error.response_status
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response({RESPONSE: {'is_liked_by_current_user': outcome.result}},
                        status=outcome.response_status)
