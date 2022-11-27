from mentor_prooject.settings import *
from photobatle.models import *
from api.status_code import *
from api.repositorys import *


class CustomPagination:
    def __init__(self, page, current_page, per_page):
        self._current_page = current_page
        self._per_page = per_page
        self._page = page

    def to_json(self):
        page = self._page
        return {
            "current_page": self._current_page or 1,
            "per_page": self._per_page or REST_FRAMEWORK["PAGE_SIZE"],
            "next_page": None
            if page.number == page.paginator.num_pages
            else page.next_page_number(),
            "prev_page": None if page.number == 1 else page.previous_page_number(),
            "total_pages": page.paginator.num_pages,
            "total_count": page.paginator.count,
        }


def can_be_deleted_and_changing_by_user(comments, user_id):
    for comment in comments:
        if comment.user.pk == user_id:
            comment.can_be_change = True
            if not CommentRepository.get_objects_by_filter(parent=comment.pk):
                comment.can_be_deleted = True
    return comments


def _like_exist(user_id, slug):
    if not user_id:
        raise ValidationError401("Missing one of all requirements parameters:api token")
    elif not slug:
        raise ValidationError400("Missing one of all requirements parameters:api slug")
    photo = PhotoRepository.get_first_object_by_filter(slug=slug)
    if not photo:
        raise ValidationError404(f"Photo with slug '{slug}' dont found")
    like = LikeRepository.get_objects_by_filter(user_id=user_id, photo_id=photo.id)
    return True if not like else False
