from rest_framework import serializers
from .models import User,Photo

class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели User'''
    class Meta:
        model=User
        fields=('__all__')

class PhotoSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Photo'''
    user_name=UserSerializer()
    class Meta:
        model=Photo
        fields=('__all__')