from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.custom_schema import *
from api.serializers import *
from api.service import *


class UserAPI(APIView):
    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=get_user_parameters,
                         responses=get_user_response, operation_description=get_user_description)
    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                GetUserService, {'user_id': request.user.id}
            )
        except Exception as e:
            return Response({'error': str(e.detail), 'status_code': str(e.status_code)}, status=e.status_code)
        return Response(ApiUserSerializer(outcome.result, many=False).data, status=status.HTTP_201_CREATED)
