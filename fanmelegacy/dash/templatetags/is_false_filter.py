from django import template
register = template.Library()


@register.filter
def is_false(arg):
    return arg is False
