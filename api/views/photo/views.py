from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from api.custom_schema import *
from photobatle import serializers
from photobatle.service import *


class PhotoAPI(APIView):
    parser_classes = [MultiPartParser, ]

    @swagger_auto_schema(responses={status.HTTP_200_OK: 'Successes'})
    def get(self, *args, **kwargs):
        serializer = serializers.PhotoSerializer(
            Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                   like_count=Count('like_photo', distinct=True)).filter(
                moderation='APR'), many=True)
        return Response(serializer.data)

    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=post_photo_parameters, responses=post_photo_response,
                         operation_description=post_photo_description)
    def post(self, request, *args, **kwargs):
        try:
            AddPhotoService.execute(request.FILES.dict() | request.POST.dict() | {'user_id': request.user.id})
        except Exception as e:
            return Response({'error': str(e.detail),
                             'status_code': str(e.status_code)}, status=e.status_code)
        return Response(status=201)


class ModifiedPhotoAPI(APIView):
    parser_classes = [MultiPartParser, ]

    @swagger_auto_schema(manual_parameters=get_photo_parameters, responses=get_photo_response)
    def get(self, *args, **kwargs):
        try:
            serializer = serializers.PhotoSerializer(
                Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                       like_count=Count('like_photo', distinct=True)).filter(
                    moderation='APR', slug=kwargs['slug']), many=True)
            if not serializer.data:
                raise ValidationError400(f"Incorrect slug_id value")
        except Exception as e:
            return Response({'error': str(e.detail),
                             'status_code': str(e.status_code)}, status=e.status_code)
        return Response(serializer.data)

    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=delete_photo_parameters, responses=delete_photo_response,
                         operation_description=delete_photo_description)
    def delete(self, request, *args, **kwargs):
        try:
            DeletePhotoService.execute(kwargs | {'user_id': request.user.id})
        except Exception as e:
            return Response({'error': str(e.detail),
                             'status_code': str(e.status_code)}, status=e.status_code)
        return Response(status=204)

    @permission_classes([IsAuthenticated])
    @swagger_auto_schema(manual_parameters=patch_photo_parameters, responses=patch_photo_response,
                         operation_description=patch_photo_operation_description)
    def patch(self, request, *args, **kwargs):
        try:
            if request.data:
                UpdatePhotoService.execute(request.data.dict() | kwargs | {'user_id': request.user.id})
            else:
                RecoveryPhotoService.execute(kwargs | {'user_id': request.user.id})
        except Exception as e:
            return Response({'error': str(e.detail),
                             'status_code': str(e.status_code)}, status=e.status_code)
        return Response(status=201)
