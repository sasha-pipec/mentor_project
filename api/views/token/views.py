from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.utils import CustomTokenAuthentication
from api.constants import *
from photobatle.service import *


class TokenAPI(APIView):
    authentication_classes = (CustomTokenAuthentication,)

    @permission_classes([IsAuthenticated])
    @swagger_auto_schema()
    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                CreateAPITokenService, {ID_OF_USER: request.user.id}
            )
        except Exception as e:
            return Response({ERROR: e.detail, STATUS_ERROR: e.status_code}, status=e.status_code)
        return Response({TOKEN: outcome.result.pk}, status=status.HTTP_201_CREATED)
