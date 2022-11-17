from rest_framework import serializers
from photobatle.models import *
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.db.models import Value

from photobatle.models import *
from api.utils import *


class ApiUsernameSerializer(serializers.ModelSerializer):
    '''User serializer'''

    class Meta:
        model = User
        fields = ('username',)

class ApiUserSerializer(serializers.ModelSerializer):
    '''User serializer'''

    all_likes = serializers.SerializerMethodField()
    all_comments = serializers.SerializerMethodField()
    api_token = serializers.SerializerMethodField()

    def get_all_likes(self, obj):
        return Like.objects.filter(user_id=obj.pk).count()

    def get_all_comments(self, obj):
        return Comment.objects.filter(user_id=obj.pk).count()

    def get_api_token(self, obj):
        return Token.objects.get(user=obj.pk).pk

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'photo', 'all_likes', 'all_comments', 'api_token')


class ApiCreateCommentSerializer(serializers.ModelSerializer):
    user = ApiUserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'photo', 'user', 'content', 'create_at',)

class ApiCommentSerializer(serializers.ModelSerializer):
    '''Comment serializer'''
    removal = serializers.BooleanField()
    change = serializers.BooleanField()
    answers = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        return str(obj.user.photo)

    def get_answers(self, obj):
        comments = Comment.objects.filter(parent=obj.id).annotate(removal=Value('user_not_authenticate'),
                                                                  change=Value('user_not_authenticate'))
        if self.context['user_id']:
            comments = get_answers_for_comments(comments, self.context['user_id'])
        return (ApiCommentSerializer(comments, context={'user_id': self.context['user_id']}, many=True)).data

    class Meta:
        model = Comment
        fields = ('id', 'photo', 'user', 'content', 'create_at', 'answers', 'change', 'removal')


class ApiPhotosSerializer(serializers.ModelSerializer):
    '''Photo serializer'''

    user = ApiUserSerializer()
    like_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()
    date_published = serializers.CharField(source='updated_at')
    name = serializers.CharField(source='photo_name')
    content = serializers.CharField(source='photo_content')

    class Meta:
        model = Photo
        fields = (
            'photo', 'name', 'content', 'user', 'like_count', 'comment_count', 'date_published', 'slug',
        )


class ApiPersonalPhotosSerializer(serializers.ModelSerializer):
    '''Photo serializer'''

    user = ApiUserSerializer()
    like_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()
    date_published = serializers.CharField(source='updated_at')
    name = serializers.CharField(source='photo_name')
    content = serializers.CharField(source='photo_content')
    status = serializers.CharField(source='get_moderation_display')
    date_published = serializers.SerializerMethodField()
    delete = serializers.SerializerMethodField()
    change = serializers.SerializerMethodField()
    recovery = serializers.SerializerMethodField()

    def get_change(self, obj):
        if obj.moderation != "DEL" and obj.moderation != "REJ":
            return True
        return False

    def get_delete(self, obj):
        if obj.moderation != "DEL" and obj.moderation != "REJ":
            return True
        return False

    def get_recovery(self, obj):
        if obj.moderation == "DEL" or obj.moderation == "REJ":
            return True
        return False

    def get_date_published(self, obj):
        if obj.moderation != "APR":
            return 'Not published'

    class Meta:
        model = Photo
        fields = (
            'photo', 'name', 'content', 'user', 'like_count', 'comment_count', 'date_published', 'status', 'slug',
            'delete', 'change', 'recovery',
        )


class ApiDetailPhotoSerializer(serializers.ModelSerializer):
    '''Photo serializer'''

    user = ApiUserSerializer()
    like_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()
    date_published = serializers.CharField(source='updated_at')
    content = serializers.CharField(source='photo_content')
    like_exist = serializers.CharField()

    class Meta:
        model = Photo
        fields = (
            'photo', 'content', 'user', 'like_count', 'comment_count', 'date_published', 'like_exist'
        )


class ApiCreatePhotoSerializers(serializers.ModelSerializer):
    user = ApiUserSerializer()

    class Meta:
        model = Photo
        fields = ('slug', 'photo_name', 'photo_content', 'create_at', 'user')


