from api.custom_schema import *
from api.service import *
from api.serializers import *
from api.metadata import *
from photobatle.service import *

from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from service_objects.services import ServiceOutcome


class PhotoAPI(APIView):
    parser_classes = [MultiPartParser, ]
    authentication_classes = (CustomTokenAuthentication,)

    @swagger_auto_schema(manual_parameters=get_home_photo_parameters, responses=get_home_photo_response)
    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                GetPhotoService, request.data.dict() if request.data else request.query_params
            )
        except Exception as error:
            return Response({ERROR: {key: value for key, value in error.errors_dict.items()},
                             STATUS_ERROR: error.response_status},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({METADATA: outcome.result['pagination_data'],
                         RESPONSE: ApiPhotosSerializer(outcome.result['photos'], context={'request': request},
                                                       many=True).data}, status=status.HTTP_200_OK)

    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=post_photo_parameters, responses=post_photo_response,
                         operation_description=post_photo_description)
    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                ApiAddPhotoService, request.POST.dict() | {ID_OF_USER: request.user.id}, request.FILES.dict()
            )
        except Exception as error:
            return Response({ERROR: {key: value for key, value in error.errors_dict.items()},
                             STATUS_ERROR: error.response_status},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(ApiCreatePhotoSerializers(outcome.result).data, status=status.HTTP_201_CREATED)


class ModifiedPhotoAPI(APIView):
    parser_classes = [MultiPartParser, ]
    metadata_class = DetailPhotoMetadata
    authentication_classes = (CustomTokenAuthentication,)

    @swagger_auto_schema(manual_parameters=get_photo_parameters, responses=get_photo_response)
    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                GetDetailPhotoService, kwargs | {ID_OF_USER: request.user.pk if request.user.is_authenticated else None}
            )
            metadata = self.metadata_class().determine_metadata(request, self)
        except Exception as e:
            return Response({ERROR: e.detail, STATUS_ERROR: e.status_code}, status=e.status_code)
        return Response({METADATA: metadata} | {RESPONSE: (
            ApiDetailPhotoSerializer(outcome.result, context={ID_OF_USER: request.user.pk if request.user.pk else None,
                                                              'request': request}, many=True).data)})

    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=delete_photo_parameters, responses=delete_photo_response,
                         operation_description=delete_photo_description)
    def delete(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                DeletePhotoService, kwargs | {ID_OF_USER: request.user.id}
            )
        except Exception as e:
            return Response({ERROR: e.detail, STATUS_ERROR: e.status_code}, status=e.status_code)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=patch_photo_parameters, responses=patch_photo_response,
                         operation_description=patch_photo_operation_description)
    def patch(self, request, *args, **kwargs):
        try:
            if request.data:
                outcome = ServiceOutcome(
                    UpdatePhotoService, request.data.dict() | kwargs | {ID_OF_USER: request.user.id}
                )
            else:
                outcome = ServiceOutcome(
                    RecoveryPhotoService, kwargs | {ID_OF_USER: request.user.id}
                )
        except Exception as e:
            return Response({ERROR: e.detail, STATUS_ERROR: e.status_code}, status=e.status_code)
        return Response(ApiCreatePhotoSerializers(outcome.result).data, status=status.HTTP_200_OK)


class PersonalPhotoAPI(APIView):
    authentication_classes = (CustomTokenAuthentication,)

    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=get_personal_photo_parameters, responses=get_personal_photo_response,
                         operation_description=get_personal_photo_description)
    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                GetPersonalPhotoService,
                request.data.dict() if request.data else request.query_params.dict() | {ID_OF_USER: request.user.pk}
            )
        except Exception as e:
            return Response({ERROR: e.detail, STATUS_ERROR: e.status_code}, status=e.status_code)
        return Response({METADATA: outcome.result['pagination_data'],
                         RESPONSE: ApiPersonalPhotosSerializer(outcome.result['photos'], context={'request': request},
                                                               many=True).data}, status=status.HTTP_200_OK)
