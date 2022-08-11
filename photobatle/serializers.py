from rest_framework import serializers
from photobatle.models import Usermodels, Photomodels, Commentmodels


class CommentSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели User'''

    class Meta:
        model = Commentmodels.Comment
        fields = ('__all__')


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
    get_moderation_display = serializers.CharField()
    all_comments = serializers.SerializerMethodField()
    photo_imagekit_medium = serializers.SerializerMethodField()

    def get_photo_imagekit_medium(self, obj):
        return obj.photo_imagekit_medium.url

    def get_all_comments(self, obj):
        return (CommentSerializer(Commentmodels.Comment.objects.select_related('photo').filter(
            photo_id=obj.id), many=True)).data

    class Meta:
        model = Photomodels.Photo
        fields = ('__all__')
