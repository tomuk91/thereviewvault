import json
from django.shortcuts import get_list_or_404, render, get_object_or_404
from .models import Review, Category
from deals.models import Deal, DealsCategory
from django.utils import timezone
from datetime import timedelta
from taggit.models import Tag
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.http import HttpResponse

# reviews/views.py


def indexnow_key(request):
    return HttpResponse("a9522e169f464f8694f4ba8856128cca", content_type="text/plain")

def twitter_callback(request):
    # Handle the OAuth callback logic here
    return HttpResponse("Twitter OAuth callback received!")

def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /secure-admin/",
        "Disallow: /admin/",
        "Disallow: /private/",
        "Disallow: /tag/",
        "Sitemap: https://www.thevaultreviews.com/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def search_reviews(request):
    query = request.GET.get('query', '').strip()
    
    # Validation checks
    if not query:
        error_message = "Please enter a search term."
        return render(request, 'reviews/search_results.html', {'error_message': error_message})

    if len(query) < 3:
        error_message = "Search term must be at least 3 characters long."
        return render(request, 'reviews/search_results.html', {'error_message': error_message})
    
    if len(query) > 100:
        error_message = "Search term is too long. Please enter a shorter search term."
        return render(request, 'reviews/search_results.html', {'error_message': error_message})
    
    # Search reviews
    reviews = Review.objects.filter(title__icontains=query)
    
    # Pagination
    paginator = Paginator(reviews, 10)  # Show 10 reviews per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'reviews': page_obj,  # Pass the paginated reviews
        'query': query,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj
    }
    return render(request, 'reviews/search_results.html', context)


def review_list(request):
    today = timezone.now()
    week_ago = today - timedelta(days=7)

    tags = Tag.objects.values_list('name', flat=True)  # Fetch only the tag names
    tags_json = json.dumps(list(tags))  # Convert QuerySet to a JSON list
    reviews = Review.objects.all().order_by('-publication_date')
    top_reviews = Review.objects.filter(publication_date__gte=week_ago).order_by('-rating')[:2]
    review_of_the_week = Review.objects.filter(review_of_the_week=True).first()
    deals_categories = DealsCategory.objects.all()
    deals = Deal.objects.all().order_by('-created_at')[:10] 
    paginator = Paginator(reviews, 6)  # Show 5 reviews per page

    page_number = request.GET.get('page')
    page_reviews = paginator.get_page(page_number)

    return render(request, 'reviews/review_list.html', {
        'tags': tags_json,
        'deals_categories': deals_categories,
        'deals': deals,
        'reviews': page_reviews,  # Pass paginated reviews to the template
        'review_of_the_week': review_of_the_week,
        'top_reviews': top_reviews,  # Pass top reviews to the template
    })


# views.py
def review_detail(request, slug):
    review = get_object_or_404(Review, slug=slug)
    title = f"{review.title} - Review Website"
    meta_description = f"Read the review of {review.title} by {review.author}. Rating: {review.rating}/5."
    meta_keywords = f"{review.title}, review, {review.author}, product reviews"

    related_reviews = Review.objects.filter(Q(category=review.category) | Q(tags__in=review.tags.all())).exclude(id=review.id).distinct()[:4]

    # related_reviews = Review.objects.filter(category=review.category).exclude(id=review.id)[:4]  # Get 4 related reviews excluding the current one

    return render(request, 'reviews/review_detail.html', {
        'review': review,
        'title': title,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
        'related_reviews': related_reviews,
        'og_image': review.image.url if review.image else '',
    })

def tagged_reviews(request, tag_slug):
    tag = Tag.objects.get(slug=tag_slug)
    reviews = Review.objects.filter(tags__in=[tag])
    
    sort_option = request.GET.get('sort', 'date')
    if sort_option == 'rating':
        reviews = reviews.order_by('-rating')
    else:
        reviews = reviews.order_by('-publication_date')
    
    # Pagination - make sure you are paginating correctly
    paginator = Paginator(reviews, 6)  # Show 6 reviews per page
    page_number = request.GET.get('page')
    page_reviews = paginator.get_page(page_number)
    
    # Handle AJAX requests for infinite scroll
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('reviews/review_list_partial.html', {'reviews': page_reviews})
        return JsonResponse({'html': html, 'has_next': page_reviews.has_next()})
    
    return render(request, 'reviews/tagged_reviews.html', {'tag': tag, 'reviews': reviews})

def reviews_by_rating(request, rating):
    try:
        # Rounding logic to include half-star ratings
        rounded_rating = round(float(rating) * 2) / 2  # Round to the nearest half
        reviews = Review.objects.filter(rating__gte=rounded_rating, rating__lt=rounded_rating + 1)

        # Sorting logic
        sort_option = request.GET.get('sort', 'date')
        if sort_option == 'rating':
            reviews = reviews.order_by('-rating')
        else:
            reviews = reviews.order_by('-publication_date')

        # Pagination logic
        paginator = Paginator(reviews, 7)  # 6 reviews per page
        page_number = request.GET.get('page', 1)
        page_reviews = paginator.get_page(page_number)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check if it's an AJAX request
            data = {
                'html': render_to_string('reviews/review_list_partial.html', {'reviews': page_reviews}),
                'has_next': page_reviews.has_next(),
            }
            return JsonResponse(data)

        return render(request, 'reviews/reviews_by_rating.html', {
            'reviews': page_reviews,
            'rating': rounded_rating,
            'message': "" if reviews else f"No reviews found for {rounded_rating}-star rating.",
        })
    except ValueError:
        return JsonResponse({'error': 'Invalid rating format.'})

@cache_page(60 * 10)  # Cache the view for 15 minutes
def category_reviews(request, slug):
    category = get_object_or_404(Category, slug=slug)
    
    # Fetch all reviews for the category
    reviews = Review.objects.filter(category=category)
    
    # Sorting logic
    sort_option = request.GET.get('sort', 'date')
    if sort_option == 'rating':
        reviews = reviews.order_by('-rating')
    else:
        reviews = reviews.order_by('-publication_date')

    # Pagination - make sure you are paginating correctly
    paginator = Paginator(reviews, 6)  # Show 6 reviews per page
    page_number = request.GET.get('page')
    page_reviews = paginator.get_page(page_number)
    
    # Handle AJAX requests for infinite scroll
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('reviews/review_list_partial.html', {'reviews': page_reviews})
        return JsonResponse({'html': html, 'has_next': page_reviews.has_next()})

    return render(request, 'reviews/category_reviews.html', {
        'category': category,
        'reviews': page_reviews,  # Paginated reviews
    })

def about_us(request):
    return render(request, 'reviews/about_us.html')

def privacy_policy(request):
    return render(request, 'reviews/privacy_policy.html')

def terms_conditions(request):
    return render(request, 'reviews/terms_conditions.html')

def contact_us(request):
    return render(request, 'reviews/contact_us.html')



def home(request):
    categories = Category.objects.all()
    return render(request, 'reviews/category_reviews.html', {'categories': categories})
