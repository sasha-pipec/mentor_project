from rest_framework import serializers
from photobatle.models import Usermodels,Photomodels


class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели User'''
    class Meta:
        model=Usermodels.User
        fields=('__all__')

class PhotoSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Photo'''
    user_name=UserSerializer()
    class Meta:
        model=Photomodels.Photo
        fields=('__all__')