from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from rest_framework.views import APIView

from api.custom_schema import *
from photobatle import serializers
from photobatle.models import User


class UserAPI(APIView):

    @swagger_auto_schema(manual_parameters=get_user_parameters,
                         responses=get_user_response)
    def get(self, request, *args, **kwargs):
        serializer = serializers.UserSerializer(
            User.objects.filter(pk=request.user.id), many=True)
        if not serializer.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=200)
