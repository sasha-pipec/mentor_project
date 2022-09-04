from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from api.custom_schema import *
from photobatle import serializers
from photobatle.service import *


class PersonalPhotoAPI(APIView):

    @swagger_auto_schema(manual_parameters=get_personal_photo_parameters, responses=get_personal_photo_response)
    def get(self, request, *args, **kwargs):
        try:
            serializer = serializers.PhotoSerializer(
                Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                       like_count=Count('like_photo', distinct=True)).filter(
                    user_id=request.user.id), many=True)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
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
            return Response(status=status.HTTP_409_CONFLICT)


class PersonalSortPhotoApi(APIView):

    @swagger_auto_schema(manual_parameters=get_sort_personal_photo_parameters,
                         responses=get_sort_personal_photo_response)
    def get(self, request, *args, **kwargs):
        try:
            data = request.data.dict() if request.data else request.query_params.dict()
            serializer = serializers.PhotoSerializer(
                PersonalSortingFormService.execute({'user_id': request.user.id} | data), many=True)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=201)
