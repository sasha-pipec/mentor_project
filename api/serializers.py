from rest_framework import serializers
from photobatle.models import *


class ApiUserSerializer(serializers.ModelSerializer):
    '''User serializer'''

    class Meta:
        model = User
        fields = ('username',)


class ApiPhotoSerializer(serializers.ModelSerializer):
    '''Photo serializer'''

    user = ApiUserSerializer()
    get_moderation_display = serializers.CharField()
    like_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()
    date_published = serializers.CharField(source='updated_at')
    name = serializers.CharField(source='photo_name')
    content = serializers.CharField(source='photo_content')

    class Meta:
        model = Photo
        fields = (
            'slug', 'photo', 'name', 'content', 'get_moderation_display', 'date_published', 'user',
            'like_count', 'comment_count'
        )
