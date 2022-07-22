from rest_framework import serializers
from photobatle.models import Usermodels, Photomodels


class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели User'''

    class Meta:
        model = Usermodels.User
        fields = ('__all__')




class PhotoSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Photo'''
    user = UserSerializer()
    like_count = serializers.IntegerField()
    comment_count = serializers.IntegerField()
    checking_the_existence = serializers.CharField()
    get_absolute_url = serializers.CharField()
    get_moderation_display=serializers.CharField()
    photo_imagekit_medium=serializers.SerializerMethodField()

    def get_photo_imagekit_medium(self,obj):
        return obj.photo_imagekit_medium.url

    class Meta:
        model = Photomodels.Photo
        fields = ('__all__')
