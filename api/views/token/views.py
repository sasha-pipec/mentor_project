from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from photobatle.service import *


class TokenAPI(APIView):
    @permission_classes([IsAuthenticated])
    @swagger_auto_schema()
    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                CreateAPITokenService, {'user_id': request.user.id}
            )
        except Exception as e:
            return Response({'error': str(e.detail),
                             'status_code': str(e.status_code)}, status=e.status_code)
        return Response({'token': outcome.result.pk}, status=200)
