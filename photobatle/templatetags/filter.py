from django import template
import os
from photobatle import models

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
def comment_count(value):
    return models.Commentmodels.Comment.objects.filter(photo=value.pk).count()

@register.filter
def like_count(value):
    return models.Likemodels.Like.objects.filter(photo_id=value.pk).count()


@register.filter
def check_like(value, arg):
    return models.Likemodels.Like.objects.filter(photo_id=arg, user_id=value).exists()


@register.filter
def list_answer_comment(value, arg):
    # возвращаем список ответов к определенному комментарию
    return value[arg - 1]


@register.filter
def author_parent_comment(value, arg):
    comment = models.Commentmodels.Comment.objects.get(pk=arg)
    return comment.user


@register.filter
def check_answer(value):
    comment_count = models.Commentmodels.Comment.objects.filter(parent_id=value)
    if len(comment_count) == 0:
        return True
    else:
        return False

@register.filter
def all_likes(value):
    return models.Likemodels.Like.objects.filter(user_id=value).count()

@register.filter
def all_comments(value):
    return models.Commentmodels.Comment.objects.filter(user_id=value).count()
