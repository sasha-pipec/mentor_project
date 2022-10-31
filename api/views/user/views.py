from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView

from api.custom_schema import *
from photobatle import serializers
from photobatle.models import User


class UserAPI(APIView):
    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=get_user_parameters,
                         responses=get_user_response, operation_description=get_user_description)
    def get(self, request, *args, **kwargs):
        serializer = serializers.UserSerializer(
            User.objects.filter(pk=request.user.id), many=True)
        if not serializer.data:
            return Response({'error': 'Incorrect value of ApiToken'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.data, status=200)
