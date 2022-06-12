from django import template
import os

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
    if os.path.isfile('media/'+str(value)):
        return True
    else:
        return False

