from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from service_objects.services import ServiceOutcome

from api.custom_schema import *
from api.serializers import ApiUserSerializer
from api.services import GetUserService
from api.utils import CustomTokenAuthentication
from api.constants import *


class UserRetrieve(RetrieveAPIView):
    authentication_classes = (CustomTokenAuthentication,)

    @swagger_auto_schema(**USER_RETRIEVE)
    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                GetUserService, {ID_OF_USER: request.user.id}
            )
        except Exception as e:
            return Response({ERROR: e.detail, STATUS_ERROR: e.status_code}, status=e.status_code)
        return Response(ApiUserSerializer(outcome.result, context={'request': request}, many=False).data,
                        status=status.HTTP_200_OK)
