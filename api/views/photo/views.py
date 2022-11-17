from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from service_objects.services import ServiceOutcome

from api.custom_schema import *
from photobatle.service import *
from api.service import *
from api.serializers import *


class PhotoAPI(APIView):
    parser_classes = [MultiPartParser, ]

    @swagger_auto_schema(manual_parameters=get_home_photo_parameters, responses=get_home_photo_response)
    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                GetPhotoService, request.data.dict() if request.data else request.query_params
            )
        except Exception as e:
            return Response({'error': str(e.detail), 'status_code': str(e.status_code)}, status=e.status_code)
        return Response(
            outcome.result['pagination_data'] | {
                'posts': ApiPhotosSerializer(outcome.result['photos'], many=True).data},
            status=status.HTTP_200_OK)

    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=post_photo_parameters, responses=post_photo_response,
                         operation_description=post_photo_description)
    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                AddPhotoService, request.FILES.dict() | request.POST.dict() | {'user_id': request.user.id}
            )
        except Exception as e:
            return Response({'error': str(e.detail),
                             'status_code': str(e.status_code)}, status=e.status_code)
        return Response(ApiCreatePhotoSerializers(outcome.result).data, status=status.HTTP_201_CREATED)


class ModifiedPhotoAPI(APIView):
    parser_classes = [MultiPartParser, ]

    @swagger_auto_schema(manual_parameters=get_photo_parameters, responses=get_photo_response)
    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                GetDetailPhotoService, kwargs | {'user_id': request.user.pk if request.user.is_authenticated else None}
            )
        except Exception as e:
            return Response({'error': str(e.detail), 'status_code': str(e.status_code)}, status=e.status_code)
        return Response(ApiDetailPhotoSerializer(outcome.result).data)

    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=delete_photo_parameters, responses=delete_photo_response,
                         operation_description=delete_photo_description)
    def delete(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                DeletePhotoService, kwargs | {'user_id': request.user.id}
            )
        except Exception as e:
            return Response({'error': str(e.detail),
                             'status_code': str(e.status_code)}, status=e.status_code)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=patch_photo_parameters, responses=patch_photo_response,
                         operation_description=patch_photo_operation_description)
    def patch(self, request, *args, **kwargs):
        try:
            if request.data:
                outcome = ServiceOutcome(
                    UpdatePhotoService, request.data.dict() | kwargs | {'user_id': request.user.id}
                )
            else:
                outcome = ServiceOutcome(
                    RecoveryPhotoService, kwargs | {'user_id': request.user.id}
                )
        except Exception as e:
            return Response({'error': str(e.detail),
                             'status_code': str(e.status_code)}, status=e.status_code)
        return Response(ApiCreatePhotoSerializers(outcome.result).data, status=status.HTTP_201_CREATED)


class PersonalPhotoAPI(APIView):
    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=get_personal_photo_parameters, responses=get_personal_photo_response,
                         operation_description=get_personal_photo_description)
    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                GetPersonalPhotoService,
                request.data.dict() if request.data else request.query_params.dict() | {"user_id": request.user.pk}
            )
        except Exception as e:
            return Response({'error': str(e.detail), 'status_code': str(e.status_code)}, status=e.status_code)
        return Response(outcome.result['pagination_data'] | {
            'posts': ApiPersonalPhotosSerializer(outcome.result['photos'], many=True).data}, status=status.HTTP_200_OK)
