from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.custom_schema import *
from photobatle import serializers
from photobatle.service import *


class PersonalPhotoAPI(APIView):
    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=get_personal_photo_parameters, responses=get_personal_photo_response,
                         operation_description=get_personal_photo_description)
    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_anonymous:
                raise ValidationError401(f"incorrect api token")
            serializer = serializers.PhotoSerializer(
                Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                       like_count=Count('like_photo', distinct=True)).filter(
                    user_id=request.user.id), many=True)
        except Exception as e:
            return Response({'error': str(e.detail),
                             'status_code': str(e.status_code)}, status=e.status_code)
        return Response(serializer.data)


class SortAndSearchPhotoApi(APIView):

    @swagger_auto_schema(manual_parameters=get_sort_photo_parameters, responses=get_sort_photo_response,
                         operation_description=get_sort_photo_operation_description)
    def get(self, request, *args, **kwargs):
        try:
            data = request.data.dict() if request.data else request.query_params
            if 'sort_value' in data:
                serializer = serializers.PhotoSerializer(SortingFormService.execute(data), many=True)
            else:
                serializer = serializers.PhotoSerializer(SearchFormService.execute(data), many=True)
            return Response(serializer.data, status=201)
        except Exception as e:
            return Response({'error': str(e.detail),
                             'status_code': str(e.status_code)}, status=e.status_code)


class PersonalSortPhotoApi(APIView):
    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=get_sort_personal_photo_parameters,
                         responses=get_sort_personal_photo_response,
                         operation_description=get_sort_personal_photo_description)
    def get(self, request, *args, **kwargs):
        try:
            data = request.data.dict() if request.data else request.query_params.dict()
            photos=(PersonalSortingFormService.execute(data | {'user_id': request.user.id}))['photos']
            serializer = serializers.PhotoSerializer((photos), many=True)
        except Exception as e:
            return Response({'error': str(e.detail),
                             'status_code': str(e.status_code)}, status=e.status_code)
        return Response(serializer.data, status=201)
