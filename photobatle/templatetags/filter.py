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

