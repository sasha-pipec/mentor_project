from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.custom_schema import *
from api.serializers import *
from api.service import *
from api.utils import CustomTokenAuthentication
from api.constants import *


class UserAPI(APIView):
    authentication_classes = (CustomTokenAuthentication,)

    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=get_user_parameters,
                         responses=get_user_response, operation_description=get_user_description)
    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                GetUserService, {ID_OF_USER: request.user.id}
            )
        except Exception as e:
            return Response({ERROR: e.detail, STATUS_ERROR: e.status_code}, status=e.status_code)
        return Response(ApiUserSerializer(outcome.result, context={'request': request}, many=False).data,
                        status=status.HTTP_200_OK)
