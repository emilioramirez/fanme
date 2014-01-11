from django import template
register = template.Library()


@register.filter
def split(str, splitter):
    return str.split(splitter)


@register.filter
def unicode(obj):
    return obj.__unicode__()


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def range(value):
    return xrange(value)
