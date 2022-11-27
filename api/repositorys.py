from django.db.models import Value, Count

from photobatle.models import Comment, Photo, Like


class DetailPhotoRepository:

    @staticmethod
    def get_objects_by_filter(like, **kwargs):
        return Photo.objects.annotate(comment_count=Count('comment_photo', distinct=True),
                                      like_count=Count('like_photo', distinct=True),
                                      is_liked_by_current_user=Value(like)).filter(**kwargs)


class PhotoRepository:

    @staticmethod
    def get_objects_by_filter(**kwargs):
        return Photo.objects.filter(**kwargs)

    @staticmethod
    def get_first_object_by_filter(**kwargs):
        return Photo.objects.filter(**kwargs).first()


class CommentRepository:

    @staticmethod
    def get_objects_by_filter(max_size=None, **kwargs):
        objects = Comment.objects.filter(**kwargs).annotate(can_be_deleted=Value(False), can_be_change=Value(False))
        return objects[:max_size if max_size else len(objects)]


class LikeRepository:

    @staticmethod
    def get_objects_by_filter(**kwargs):
        return Like.objects.filter(**kwargs)
