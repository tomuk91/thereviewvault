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

@register.filter
def get_attr(obj, attr_name):
    """Get an attribute of an object dynamically."""
    try:
        return getattr(obj, attr_name)
    except (AttributeError, TypeError):
        return None