from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_stars(rating, max_stars=5):
    """Renders star icons for a given rating with accessibility features."""
    full_star = '<i class="fas fa-star" aria-hidden="true"></i>'
    half_star = '<i class="fas fa-star-half-alt" aria-hidden="true"></i>'
    empty_star = '<i class="far fa-star" aria-hidden="true"></i>'
    
    stars_html = ''
    for i in range(1, max_stars + 1):
        if rating >= i:
            stars_html += full_star  # Full star
        elif rating >= i - 0.5:
            stars_html += half_star  # Half star
        else:
            stars_html += empty_star  # Empty star

    # Add accessible text for screen readers
    accessible_text = f'<span class="sr-only">Rated {rating} out of {max_stars} stars</span>'
    
    return mark_safe(stars_html + accessible_text)
