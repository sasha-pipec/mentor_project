from api.utils import *
from api.constants import *
from api.repositorys import *

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from photobatle.models import *


class ApiUsernameSerializer(serializers.ModelSerializer):
    """Username serializer"""

    class Meta:
        model = User
        fields = ('username',)


class ApiUserSerializer(serializers.ModelSerializer):
    """User serializer"""

    all_likes = serializers.SerializerMethodField()
    all_comments = serializers.SerializerMethodField()
    api_token = serializers.SerializerMethodField()

    @staticmethod
    def get_all_likes(obj):
        return Like.objects.filter(user_id=obj.pk).count()

    @staticmethod
    def get_all_comments(obj):
        return Comment.objects.filter(user_id=obj.pk).count()

    @staticmethod
    def get_api_token(obj):
        return Token.objects.get(user=obj.pk).pk

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'photo', 'all_likes', 'all_comments', 'api_token')


class ApiCreateCommentSerializer(serializers.ModelSerializer):
    """Create comment serializer"""

    user = ApiUsernameSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'photo', 'user', 'content', 'create_at', 'parent')


class ApiCommentSerializer(serializers.ModelSerializer):
    """Comment serializer"""
    user = ApiUsernameSerializer()
    can_be_deleted = serializers.BooleanField()
    can_be_change = serializers.BooleanField()
    answers = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    @staticmethod
    def get_photo(obj):
        return str(obj.user.photo)

    def get_answers(self, obj):
        comments = CommentRepository.get_objects_by_filter(parent=obj.id)
        if self.context['user_id']:
            comments = can_be_deleted_and_changing_by_user(comments, self.context['user_id'])
        return (ApiCommentSerializer(comments, context={'user_id': self.context['user_id']}, many=True)).data

    class Meta:
        model = Comment
        fields = ('id', 'photo', 'user', 'content', 'create_at', 'parent', 'answers', 'can_be_change', 'can_be_deleted')


class ApiPhotosSerializer(serializers.ModelSerializer):
    """Photo serializer"""

    user = ApiUsernameSerializer()
    like_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()
    name = serializers.CharField(source='photo_name')
    content = serializers.CharField(source='photo_content')

    class Meta:
        model = Photo
        fields = (
            'photo', 'name', 'content', 'user', 'like_count', 'comment_count', 'published_at', 'slug',
        )


class ApiPersonalPhotosSerializer(serializers.ModelSerializer):
    """Personal photo serializer"""

    user = ApiUsernameSerializer()
    like_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()
    name = serializers.CharField(source='photo_name')
    content = serializers.CharField(source='photo_content')
    status = serializers.CharField(source='get_moderation_display')
    date_published = serializers.SerializerMethodField()
    delete = serializers.SerializerMethodField()
    change = serializers.SerializerMethodField()
    recovery = serializers.SerializerMethodField()

    @staticmethod
    def get_change(obj):
        if obj.moderation != Photo.ON_DELETION and obj.moderation != Photo.REJECTED:
            return True
        return False

    @staticmethod
    def get_delete(obj):
        if obj.moderation != Photo.ON_DELETION and obj.moderation != Photo.REJECTED:
            return True
        return False

    @staticmethod
    def get_recovery(obj):
        if obj.moderation == Photo.ON_DELETION or obj.moderation == Photo.ON_MODERATION:
            return True
        return False

    @staticmethod
    def get_date_published(obj):
        if obj.moderation != Photo.APPROVED:
            return 'Not published'
        return obj.published_at

    class Meta:
        model = Photo
        fields = (
            'photo', 'name', 'content', 'user', 'like_count', 'comment_count', 'date_published', 'status', 'slug',
            'delete', 'change', 'recovery',
        )


class ApiDetailPhotoSerializer(serializers.ModelSerializer):
    """ Detail photo serializer"""

    user = ApiUsernameSerializer()
    like_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()
    content = serializers.CharField(source='photo_content')
    is_liked_by_current_user = serializers.CharField()
    the_first_three_comments = serializers.SerializerMethodField()

    def get_the_first_three_comments(self, obj):
        comments = CommentRepository.get_objects_by_filter(MAX_NUMBER_OF_COMMENTS_FOR_DETAIL_PHOTO,
                                                           photo_id=obj.id, parent=None)
        if self.context['user_id']:
            comments = can_be_deleted_and_changing_by_user(comments, self.context['user_id'])
        return (ApiCommentSerializer(comments, context={'user_id': self.context['user_id']}, many=True)).data

    class Meta:
        model = Photo
        fields = (
            'photo', 'content', 'user', 'like_count', 'comment_count', 'published_at', 'is_liked_by_current_user',
            'the_first_three_comments'
        )


class ApiCreatePhotoSerializers(serializers.ModelSerializer):
    """Create photo serializer"""
    user = ApiUsernameSerializer()

    class Meta:
        model = Photo
        fields = ('slug', 'photo_name', 'photo_content', 'create_at', 'user')
