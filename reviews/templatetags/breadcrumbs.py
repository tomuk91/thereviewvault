from django import template
from django.urls import reverse
from django.utils.html import format_html
from reviews.models import Review, Category  # Import your models

register = template.Library()

@register.simple_tag(takes_context=True)
def breadcrumbs(context):
    request = context['request']
    path = request.path.strip('/').split('/')

    breadcrumb_list = []
    url_accumulator = ""
    
    # Home link
    breadcrumb_list.append(f'<li class="breadcrumb-item"><a href="{reverse("review_list")}">Home</a></li>')

    for index, segment in enumerate(path):
        url_accumulator += f"/{segment}"
        
        # Check if it's a category page
        if segment == 'category':
            category_slug = path[index + 1] if len(path) > index + 1 else None
            if category_slug:
                try:
                    category = Category.objects.get(slug=category_slug)
                    breadcrumb_list.append(
                        f'<li class="breadcrumb-item"><a href="{reverse("category_reviews", args=[category.slug])}">{category.name}</a></li>'
                    )
                except Category.DoesNotExist:
                    pass  # If category is not found, skip it
                
        # Check if it's a review page
        elif segment == 'review':
            review_slug = path[index + 1] if len(path) > index + 1 else None
            if review_slug:
                try:
                    review = Review.objects.get(slug=review_slug)
                    breadcrumb_list.append(
                        f'<li class="breadcrumb-item active" aria-current="page">{review.title}</li>'
                    )
                except Review.DoesNotExist:
                    pass  # If review is not found, skip it

    return format_html(''.join(breadcrumb_list))
