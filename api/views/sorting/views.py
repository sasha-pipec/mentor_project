from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from api.custom_schema import *
from photobatle.serializers import *
from photobatle.service import *


class PersonalPhotoAPI(APIView):
    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=get_personal_photo_parameters, responses=get_personal_photo_response,
                         operation_description=get_personal_photo_description)
    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_anonymous:
                raise ValidationError401(f"incorrect api token")
            serializer = PhotoSerializer(
                Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                       like_count=Count('like_photo', distinct=True)).filter(
                    user_id=request.user.id), many=True)
        except Exception as e:
            return Response({'error': str(e.detail), 'status_code': str(e.status_code)}, status=e.status_code)
        return Response(serializer.data)


class PersonalSortPhotoApi(APIView):
    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=get_sort_personal_photo_parameters,
                         responses=get_sort_personal_photo_response,
                         operation_description=get_sort_personal_photo_description)
    def get(self, request, *args, **kwargs):
        try:
            outcome = ServiceOutcome(
                PersonalSortingFormService,
                request.data.dict() if request.data else request.query_params.dict() | {'user_id': request.user.pk}
            )
        except Exception as e:
            return Response({'error': str(e.detail), 'status_code': str(e.status_code)}, status=e.status_code)
        return Response(PhotoSerializer(outcome.result['photos'], many=True).data, status=201)
