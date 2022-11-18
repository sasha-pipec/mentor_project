from rest_framework import serializers

from api.serializers import *

class PhotoSerializer(serializers.ModelSerializer):
    '''Photo serializer'''
    user = ApiUsernameSerializer()
    like_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()
    checking_the_existence = serializers.CharField()
    get_absolute_url = serializers.CharField()
    get_moderation_display = serializers.CharField()
    photo_imagekit_medium = serializers.SerializerMethodField()

    def get_photo_imagekit_medium(self, obj):
        return obj.photo_imagekit_medium.url

    class Meta:
        model = Photo
        fields = ('__all__')
