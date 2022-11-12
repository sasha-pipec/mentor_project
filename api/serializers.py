from rest_framework import serializers
from photobatle.models import *


class ApiPhotoSerializer(serializers.ModelSerializer):
    '''Photo serializer'''

    get_moderation_display = serializers.CharField()

    class Meta:
        model = Photo
        fields = ('slug', 'photo', 'photo_name', 'photo_content', 'get_moderation_display', 'user')
