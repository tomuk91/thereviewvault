from django import template

register = template.Library()

@register.filter
def remove_www(value):
    """Removes 'www.' from the given URL."""
    return value.replace('www.', '')

@register.filter
def remove_review(value):
    """Removes 'www.' from the given URL."""
    return value.replace('Review', '')
