from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions

from mentor_prooject.settings import *

from api.repositorys import *


class CustomTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token, make sure it is up-to-date and valid')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        return (token.user, token)


class CustomPagination:
    def __init__(self, page, current_page, per_page):
        self._current_page = int(current_page)
        self._per_page = int(per_page)
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
