from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from photobatle import serializers
from photobatle.service import *
from photobatle import models

from .custom_schema import *

from drf_yasg.utils import swagger_auto_schema


class UserAPI(APIView):

    @swagger_auto_schema(manual_parameters=get_user_parameters,
                         responses=get_user_response)
    def get(self, request, *args, **kwargs):
        serializer = serializers.UserSerializer(
            models.Usermodels.User.objects.filter(pk=request.user.id), many=True)
        if not serializer.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=200)


class PhotoAPI(APIView):
    parser_classes = [MultiPartParser, ]

    @swagger_auto_schema(responses={status.HTTP_200_OK: 'Successes'})
    def get(self, *args, **kwargs):
        serializer = serializers.PhotoSerializer(
            models.Photomodels.Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                      like_count=Count('like_photo', distinct=True)).filter(
                moderation='APR'), many=True)
        return Response(serializer.data)

    @swagger_auto_schema(manual_parameters=post_photo_parameters, responses=post_photo_response)
    def post(self, request, *args, **kwargs):
        try:
            AddPhotoService.execute(request.FILES.dict() | request.POST.dict() | {'user_id': request.user.id})
        except Exception as error:
            return Response(status=status.HTTP_409_CONFLICT)
        return Response(status=201)


class PersonalPhotoAPI(APIView):

    def get(self, request, *args, **kwargs):
        try:
            serializer = serializers.PhotoSerializer(
                models.Photomodels.Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                          like_count=Count('like_photo', distinct=True)).filter(
                    user_id=request.user.id), many=True)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)


class ModifiedPhotoAPI(APIView):
    parser_classes = [MultiPartParser, ]

    @swagger_auto_schema(manual_parameters=get_photo_parameters, responses=get_photo_response)
    def get(self, *args, **kwargs):
        try:
            serializer = serializers.PhotoSerializer(
                models.Photomodels.Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                                          like_count=Count('like_photo', distinct=True)).filter(
                    moderation='APR', slug=kwargs['slug_id']), many=True)
            if not serializer.data:
                raise Exception(f"Incorrect slug_id value")
        except Exception:
            return Response(status=status.HTTP_409_CONFLICT)
        return Response(serializer.data)

    @swagger_auto_schema(manual_parameters=delete_photo_parameters, responses=delete_photo_response)
    def delete(self, request, *args, **kwargs):
        try:
            DeletePhotoService.execute(kwargs | {'user_id': request.user.id})
        except Exception:
            return Response(status=status.HTTP_409_CONFLICT)
        return Response(status=204)

    @swagger_auto_schema(manual_parameters=patch_photo_parameters, responses=patch_photo_response,
                         operation_description=patch_photo_operation_description)
    def patch(self, request, *args, **kwargs):
        try:
            if request.data:
                UpdatePhotoService.execute(request.data.dict() | kwargs | {'user_id': request.user.id})
            else:
                RecoveryPhotoService.execute(kwargs | {'user_id': request.user.id})
        except Exception as e:
            return Response(status=status.HTTP_409_CONFLICT)
        return Response(status=201)


class SortAndSearchPhotoApi(APIView):

    def get(self, request, *args, **kwargs):
        try:
            if 'form' in request.data:
                serializer = serializers.PhotoSerializer(SortingFormService.execute(request.data.dict()), many=True)
            else:
                serializer = serializers.PhotoSerializer(SearchFormService.execute(request.data.dict()), many=True)
            return Response(serializer.data, status=201)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PersonalSortPhotoApi(APIView):

    def get(self, request, *args, **kwargs):
        try:
            serializer = serializers.PhotoSerializer(
                PersonalSortingFormService.execute(request.data.dict() | {'user_id': request.user.id}), many=True)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=201)


class CommentAPI(APIView):

    def get(self, *args, **kwargs):
        serializer = serializers.CommentSerializer(
            models.Commentmodels.Comment.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            CreateCommentService.execute(request.data.dict() | {'user_id': request.user.id})
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=201)


class ModifiedCommentAPI(APIView):

    def delete(self, request, *args, **kwargs):
        try:
            DeleteCommentService.execute(kwargs | {'user_id': request.user.id})
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=204)

    def patch(self, request, *args, **kwargs):
        try:
            UpdateCommentService.execute(request.data.dict() | kwargs | {'user_id': request.user.id})
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=201)


class LikeAPI(APIView):

    def post(self, request, *args, **kwargs):
        try:
            CreateLikeService.execute(request.data.dict() | {'user_id': request.user.id})
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=201)


class ModifiedLikeAPI(APIView):
    def delete(self, request, *args, **kwargs):
        try:
            DeleteLikeService.execute(kwargs | {'user_id': request.user.id})
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=204)

    # Create your views here.
