from rest_framework import serializers

from api.query_objects import CommentRepository
from api.serializers.users import ApiUsernameSerializer
from api.utils import can_be_deleted_and_changing_by_user
from photobatle.models import Comment


class ApiCreateCommentSerializer(serializers.ModelSerializer):
    """Create comment serializer"""

    user = ApiUsernameSerializer()
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'create_at', 'parent')


class ApiCommentSerializer(serializers.ModelSerializer):
    """Comment serializer"""
    user = ApiUsernameSerializer()
    can_be_deleted = serializers.BooleanField()
    can_be_change = serializers.BooleanField()
    answers = serializers.SerializerMethodField()

    def get_answers(self, obj):
        comments = CommentRepository.get_objects_by_filter(parent=obj.id)
        if self.context['user_id']:
            comments = can_be_deleted_and_changing_by_user(comments, self.context['user_id'])
        return (ApiCommentSerializer(comments, context={'user_id': self.context['user_id'],
                                                        'request': self.context['request']}, many=True)).data

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'create_at', 'parent', 'answers', 'can_be_change', 'can_be_deleted')