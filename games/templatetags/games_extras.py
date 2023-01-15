from django import template

register = template.Library()


@register.filter
def humaize_inclusive_range(value):
    if value.lower == value.upper:
        return value.lower
    return f"{value.lower} - {value.upper}"
