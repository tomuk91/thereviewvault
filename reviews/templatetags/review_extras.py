from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_stars(rating, max_stars=5):
    """Renders star icons for a given rating with decimals, including half stars."""
    full_star = '<i class="fas fa-star" aria-hidden="true"></i>'
    half_star = '<i class="fas fa-star-half-alt" aria-hidden="true"></i>'
    empty_star = '<i class="far fa-star" aria-hidden="true"></i>'
    
    stars_html = ''
    # Loop through each star position
    for i in range(1, max_stars + 1):
        if rating >= i:
            stars_html += full_star  # Full star if rating is greater than or equal to current star position
        elif i - rating <= 0.5:
            stars_html += half_star  # Half star if the difference between current star and rating is <= 0.5
        else:
            stars_html += empty_star  # Empty star otherwise

    # Add accessible text for screen readers
    accessible_text = f'<span class="sr-only">Rated {rating} out of {max_stars} stars</span>'
    
    return mark_safe(stars_html + accessible_text)
