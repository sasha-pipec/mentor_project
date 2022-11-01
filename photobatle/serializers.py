from rest_framework import serializers
from photobatle.models import *


class CommentSerializer(serializers.ModelSerializer):
    '''Comment serializer'''

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'create_at')


class UserSerializer(serializers.ModelSerializer):
    '''User serializer'''

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class PhotoSerializer(serializers.ModelSerializer):
    '''Photo serializer'''
    user = UserSerializer()
    like_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()
    checking_the_existence = serializers.CharField()
    get_absolute_url = serializers.CharField()
    get_moderation_display = serializers.CharField()
    all_comments = serializers.SerializerMethodField()
    photo_imagekit_medium = serializers.SerializerMethodField()

    def get_photo_imagekit_medium(self, obj):
        return obj.photo_imagekit_medium.url

    def get_all_comments(self, obj):
        return (CommentSerializer(Comment.objects.select_related('photo').filter(
            photo_id=obj.id), many=True)).data

    class Meta:
        model = Photo
        fields = ('__all__')
