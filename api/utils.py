from mentor_prooject.settings import *
from photobatle.models import Comment
from photobatle.serializers import *
from api.status_code import *


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


def get_answers_for_comments(comments, user_id):
    for comment in comments:
        if comment.user.pk == user_id:
            comment.change = True
            if Comment.objects.filter(parent=comment.pk):
                comment.removal = False
            else:
                comment.removal = True
        else:
            comment.change = False
            comment.removal = False
    return comments


def check_like(user_id, slug):
    try:
        if not user_id:
            raise ValidationError401(f'Incorrect value of api token')
        photo = Photo.objects.get(slug=slug)
        like = Like.objects.filter(user_id=user_id, photo_id=photo.id)
        return True if not like else False
    except Exception:
        raise ValidationError404(f'Incorrect value of slug or api_token')
