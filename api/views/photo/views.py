from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from service_objects.services import ServiceOutcome

from api.constants import *
from api.custom_schema import *
from api.services import GetPhotoService, ApiAddPhotoService, GetDetailPhotoService, GetPersonalPhotoService
from api.serializers import ApiPhotosSerializer, ApiCreatePhotoSerializers, ApiDetailPhotoSerializer, \
    ApiPersonalPhotosSerializer
from api.metadata import *
from api.utils import CustomTokenAuthentication, CustomPagination
from mentor_prooject.settings import REST_FRAMEWORK
from photobatle.services import DeletePhotoService, RecoveryPhotoService, UpdatePhotoService


class PhotoListCreateView(ListCreateAPIView):
    parser_classes = [MultiPartParser, ]
    authentication_classes = (CustomTokenAuthentication,)

    @swagger_auto_schema(**GENERAL_PHOTO_LIST)
    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                GetPhotoService, request.data.dict() if request.data else request.query_params
            )
        except Exception as error:
            return Response(
                {
                    ERROR: {key: value for key, value in error.errors_dict.items()},
                    STATUS_ERROR: error.response_status
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                METADATA: {'Pagination': CustomPagination(
                    outcome.result,
                    request.data.get('page') or request.query_params.get('page') or 1,
                    request.data.get('per_page') or request.query_params.get('per_page') or REST_FRAMEWORK["PAGE_SIZE"]
                ).to_json()},
                RESPONSE: ApiPhotosSerializer(outcome.result, context={'request': request}, many=True).data
            }, status=status.HTTP_200_OK)

    @swagger_auto_schema(**PHOTO_CREATE)
    def post(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                ApiAddPhotoService, request.POST.dict() | {ID_OF_USER: request.user.id}, request.FILES.dict()
            )
        except Exception as error:
            return Response(
                {
                    ERROR: {key: value for key, value in error.errors_dict.items()},
                    STATUS_ERROR: error.response_status
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(ApiCreatePhotoSerializers(outcome.result).data, status=status.HTTP_201_CREATED)


class PhotoRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser, ]
    metadata_class = DetailPhotoMetadata
    authentication_classes = (CustomTokenAuthentication,)
    http_method_names = ["patch", "get", "delete"]

    @swagger_auto_schema(**PHOTO_RETRIEVE)
    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                GetDetailPhotoService, kwargs | {ID_OF_USER: request.user.pk if request.user.is_authenticated else None}
            )
        except Exception as e:
            return Response({ERROR: e.detail, STATUS_ERROR: e.status_code}, status=e.status_code)
        return Response(
            {
                METADATA: self.metadata_class().determine_metadata(request, self),
                RESPONSE: (ApiDetailPhotoSerializer(outcome.result, context={
                    ID_OF_USER: request.user.pk if request.user.pk else None,
                    'request': request
                }, many=False).data)
            }, status=status.HTTP_200_OK)

    @swagger_auto_schema(**PHOTO_DELETE)
    def delete(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                DeletePhotoService, kwargs | {ID_OF_USER: request.user.id}
            )
        except Exception as e:
            return Response({ERROR: e.detail, STATUS_ERROR: e.status_code}, status=e.status_code)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(**PHOTO_PATCH)
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


class PersonalPhotoListView(ListAPIView):
    authentication_classes = (CustomTokenAuthentication,)

    @swagger_auto_schema(**PERSONAL_PHOTO_LIST)
    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                GetPersonalPhotoService,
                request.data.dict() if request.data else request.query_params.dict() | {ID_OF_USER: request.user.pk}
            )
        except Exception as e:
            return Response({ERROR: e.detail, STATUS_ERROR: e.status_code}, status=e.status_code)
        return Response(
            {
                METADATA: {'Pagination': CustomPagination(
                    outcome.result,
                    request.data.get('page') or request.query_params.get('page') or 1,
                    request.data.get('per_page') or request.query_params.get('per_page') or REST_FRAMEWORK["PAGE_SIZE"]
                ).to_json()},
                RESPONSE: ApiPersonalPhotosSerializer(outcome.result, context={'request': request}, many=True).data
            }, status=status.HTTP_200_OK)
