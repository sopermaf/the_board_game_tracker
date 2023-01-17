from django import template
from django.http.request import HttpRequest

register = template.Library()


@register.filter
def humaize_inclusive_range(value):
    if value.lower == value.upper:
        return value.lower
    return f"{value.lower} - {value.upper}"


@register.simple_tag
def extend_querystring(request: HttpRequest, **kwargs):
    """Makes a urlencoded querystring with the extra parameters"""
    new_params = request.GET.copy()
    new_params.update(kwargs)

    return new_params.urlencode()
