from django import template

register = template.Library()


@register.filter
def humaize_inclusive_range(value):
    return f"{value.lower} - {value.upper}"
