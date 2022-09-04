from django import template
import os
from photobatle.models import *

register = template.Library()


@register.filter
def len_name(value):
    return len(value) >= 11


@register.filter
def first_letters(value):
    return value[0:8]


@register.filter
def check_photo(value):
    return os.path.exists(str(value)[1::])


@register.filter
def check_photo_admin(value):
    return bool(value)


@register.filter
def comment_count(value):
    return Comment.objects.filter(photo=value.pk).count()


@register.filter
def like_count(value):
    return Like.objects.filter(photo_id=value.pk).count()


@register.filter
def check_like(value, arg):
    return Like.objects.filter(photo_id=arg, user_id=value).exists()


@register.filter
def list_answer_comment(value, arg):
    # return list answers for certain comment
    return value[arg - 1]


@register.filter
def author_parent_comment(value, arg):
    comment = Comment.objects.get(pk=arg)
    return comment.user


@register.filter
def check_answer(value):
    comment_count = Comment.objects.filter(parent_id=value)
    if len(comment_count) == 0:
        return True
    else:
        return False


@register.filter
def all_likes(value):
    return Like.objects.filter(user_id=value).count()


@register.filter
def all_comments(value):
    return Comment.objects.filter(user_id=value).count()
