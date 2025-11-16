from django import template

register = template.Library()

@register.filter
def abs_val(value):
    return abs(value)
