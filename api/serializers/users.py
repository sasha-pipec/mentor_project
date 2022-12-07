from rest_framework import serializers
from rest_framework.authtoken.models import Token

from api.constants import DEFAULT_PHOTO_PATH
from photobatle.models import User, Like, Comment


class ApiUsernameSerializer(serializers.ModelSerializer):
    """Username serializer"""

    class Meta:
        model = User
        fields = ('username', 'photo')


class ApiUserSerializer(serializers.ModelSerializer):
    """User serializer"""

    all_likes = serializers.SerializerMethodField()
    all_comments = serializers.SerializerMethodField()
    api_token = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        request = self.context['request']
        try:
            photo_url = obj.photo.url
        except:
            photo_url = DEFAULT_PHOTO_PATH
        return request.build_absolute_uri(photo_url)

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