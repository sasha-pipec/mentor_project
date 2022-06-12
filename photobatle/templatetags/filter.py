from django import template

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