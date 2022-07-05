from django import template
import os
from photobatle import models

register = template.Library()

@register.filter
def len_name(value):
    if len(value)>=11:
        return True
    else:
        return False

@register.filter
def first_letters(value):
    return value[0:8]


@register.filter
def check_photo(value):
    if os.path.exists(  str(value)[1::]):
        return True
    else:
        return False

@register.filter
def comment_count(value):
    comment_count=models.Commentmodels.Comment.objects.filter(photo=value.pk).count()
    return comment_count


@register.filter
def list_answer_comment(value,arg):
    #возвращаем список ответов к определенному комментарию
    return value[arg-1]

@register.filter
def author_parent_comment(value,arg):
    comment=models.Commentmodels.Comment.objects.get(pk=arg)
    return comment.user_name

@register.filter
def check_answer(value):
    comment_count=models.Commentmodels.Comment.objects.filter(parent_id=value)
    if len(comment_count)==0:
        return True
    else:
        return False

