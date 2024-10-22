import json
from django.shortcuts import get_list_or_404, render, get_object_or_404
from .models import Review, Category
from deals.models import Deal, DealsCategory
from django.utils import timezone
from datetime import timedelta
from taggit.models import Tag
from django.db.models import Q, Count
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils.timezone import now


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
        "Disallow: /search/",
        "Disallow: /hot-reviews/",
        "Disallow: /*?sort=date",
        "Disallow: /*?sort=rating",
        "Disallow: /*?page=",
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
    reviews = Review.objects.filter(title__icontains=query, publication_date__lte=timezone.now())

    # Pagination
    paginator = Paginator(reviews, 10)  # Show 10 reviews per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Meta description and keywords for SEO
    meta_description = f"Search results for '{query}'. Find detailed reviews and ratings of products matching your search query."
    meta_keywords = f"search, {query}, product reviews, {query} reviews, product ratings, review search results"
    title = f"Search Results for '{query}'"

    context = {
        'title': title,
        'reviews': page_obj,  # Pass the paginated reviews
        'query': query,
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
    }
    return render(request, 'reviews/search_results.html', context)



def review_list(request):
    today = timezone.now()
    week_ago = today - timedelta(days=7)
    og_image = '/media/review_images/logo1.webp'
    title = "TheVaultReviews | Unbiased Reviews & Deals"
    tags = Tag.objects.values_list('name', flat=True)  # Fetch only the tag names
    tags_json = json.dumps(list(tags))  # Convert QuerySet to a JSON list
    reviews = Review.objects.filter(publication_date__lte=timezone.now()).order_by('-publication_date')
    top_reviews = Review.objects.filter(publication_date__gte=week_ago, publication_date__lte=timezone.now()).order_by('-rating')[:2]
    review_of_the_week = Review.objects.filter(review_of_the_week=True).first()
    deals_categories = DealsCategory.objects.all()
    deals = Deal.objects.all().order_by('-created_at')[:10] 
    paginator = Paginator(reviews, 6)  # Show 6 reviews per page

    page_number = request.GET.get('page')
    page_reviews = paginator.get_page(page_number)

    # Meta description and keywords for SEO
    meta_description = "Discover the latest product reviews, top-rated gadgets, and exclusive deals. Find in-depth reviews and comparisons on tech, gaming, smart home devices, and more."
    meta_keywords = "product reviews, best tech gadgets, gaming reviews, smart home devices, latest deals, top-rated products, comparison reviews, affordable tech"

    return render(request, 'reviews/review_list.html', {
        'title': title,
        'og_image': og_image,
        'tags': tags_json,
        'deals_categories': deals_categories,
        'deals': deals,
        'reviews': page_reviews,  # Pass paginated reviews to the template
        'review_of_the_week': review_of_the_week,
        'top_reviews': top_reviews,  # Pass top reviews to the template
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
    })



# views.py
def review_detail(request, slug):
    review = get_object_or_404(Review, slug=slug, publication_date__lte=timezone.now())
    title = f"{review.title} | The Vault Reviews"
    content_snippet = review.content[:147]  # Get the first 150 characters of the review content
    meta_description = f"{content_snippet}"
    meta_keywords = f"{review.title}, review, {review.author}, {review.category}, {', '.join(tag.name for tag in review.tags.all() if tag in review.tags.all())}, product reviews"
    related_reviews = Review.objects.filter(Q(category=review.category) | Q(tags__in=review.tags.all()), publication_date__lte=timezone.now()).exclude(id=review.id).distinct()[:3]
    review.views += 1  # Increment the view count
    review.save(update_fields=['views'])  # Save the view count
    # related_reviews = Review.objects.filter(category=review.category).exclude(id=review.id)[:4]  # Get 4 related reviews excluding the current one

    return render(request, 'reviews/review_detail.html', {
        'title': title,
        'review': review,
        'title': title,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
        'related_reviews': related_reviews,
        'og_image': review.image.url if review.image else '',
    })

def tagged_reviews(request, tag_slug):
    tag = Tag.objects.get(slug=tag_slug)
    reviews = Review.objects.filter(tags__in=[tag], publication_date__lte=timezone.now())
    
    sort_option = request.GET.get('sort', 'date')
    if sort_option == 'rating':
        reviews = reviews.order_by('-rating')
    else:
        reviews = reviews.order_by('-publication_date')
    
    # Pagination - make sure you are paginating correctly
    paginator = Paginator(reviews, 6)  # Show 6 reviews per page
    page_number = request.GET.get('page')
    page_reviews = paginator.get_page(page_number)
    
    # Meta description and keywords
    meta_description = f"Explore reviews tagged with {tag.name}. Read detailed analysis and ratings of products in the {tag.name} category."
    meta_keywords = f"{tag.name}, product reviews, {', '.join(review.title for review in reviews)}, best {tag.name} reviews"
    title = f"Reviews Tagged with '{tag.name}' | The Vault Reviews"
    
    # Handle AJAX requests for infinite scroll
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('reviews/review_list_partial.html', {'reviews': page_reviews})
        return JsonResponse({'html': html, 'has_next': page_reviews.has_next()})
    
    return render(request, 'reviews/tagged_reviews.html', {
        'title': title,
        'tag': tag,
        'reviews': reviews,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
    })


def reviews_by_rating(request, rating):
    try:
        # Rounding logic to include half-star ratings
        rounded_rating = round(float(rating) * 2) / 2  # Round to the nearest half
        reviews = Review.objects.filter(rating__gte=rounded_rating, rating__lt=rounded_rating + 1, publication_date__lte=timezone.now())

        # Sorting logic
        sort_option = request.GET.get('sort', 'date')
        if sort_option == 'rating':
            reviews = reviews.order_by('-rating')
        else:
            reviews = reviews.order_by('-publication_date')

        # Pagination logic
        paginator = Paginator(reviews, 7)  # 7 reviews per page
        page_number = request.GET.get('page', 1)
        page_reviews = paginator.get_page(page_number)

        # Meta description and keywords
        meta_description = f"Browse top-rated product reviews with {rounded_rating}-star ratings. Find detailed insights and ratings for a variety of products."
        meta_keywords = f"{rounded_rating}-star reviews, top-rated products, product reviews, best {rounded_rating}-star products"
        title = f"Reviews with {rounded_rating}-Star Rating | The Vault Reviews"

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check if it's an AJAX request
            data = {
                'html': render_to_string('reviews/review_list_partial.html', {'reviews': page_reviews}),
                'has_next': page_reviews.has_next(),
            }
            return JsonResponse(data)

        return render(request, 'reviews/reviews_by_rating.html', {
            'title': title,
            'reviews': page_reviews,
            'rating': rounded_rating,
            'message': "" if reviews else f"No reviews found for {rounded_rating}-star rating.",
            'meta_description': meta_description,
            'meta_keywords': meta_keywords,
        })
    except ValueError:
        return JsonResponse({'error': 'Invalid rating format.'})


@cache_page(60 * 10)  # Cache the view for 15 minutes
def category_reviews(request, slug):
    category = get_object_or_404(Category, slug=slug)
    
    # Fetch all reviews for the category
    reviews = Review.objects.filter(category=category, publication_date__lte=timezone.now())
    
    # Sorting logic
    sort_option = request.GET.get('sort', 'date')
    if sort_option == 'rating':
        reviews = reviews.order_by('-rating')
    else:
        reviews = reviews.order_by('-publication_date')

    # Pagination - 6 reviews per page
    paginator = Paginator(reviews, 6)
    page_number = request.GET.get('page')
    page_reviews = paginator.get_page(page_number)
    
    # Meta description and keywords
    meta_description = f"Explore in-depth reviews of products in the {category.name} category. Find top-rated products and expert reviews on {category.name} items."
    meta_keywords = f"{category.name} reviews, top {category.name} products, {category.name} product reviews, best {category.name} products"
    title = f"Reviews in {category.name} Category | The Vault Reviews"

    # Handle AJAX requests for infinite scroll
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('reviews/review_list_partial.html', {'reviews': page_reviews})
        return JsonResponse({'html': html, 'has_next': page_reviews.has_next()})

    return render(request, 'reviews/category_reviews.html', {
        'title': title,
        'category': category,
        'reviews': page_reviews,  # Paginated reviews
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
    })



def hot_reviews(request):
    one_week_ago = now() - timedelta(days=7)
    reviews = Review.objects.filter(publication_date__gte=one_week_ago, publication_date__lte=timezone.now()).order_by('-views')[:5]

    # Meta description and keywords
    meta_description = "Check out the hottest reviews of the week! Discover the most-viewed and top-rated products reviewed in the past 7 days."
    meta_keywords = "hot reviews, most popular reviews, top reviews of the week, trending product reviews, best-reviewed products"
    title = "Hottest Reviews of the Week | The Vault Reviews"
    
    return render(request, 'reviews/hot_reviews.html', {
        'title': title,
        'reviews': reviews,  # Top 5 most-viewed reviews
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
    })



def about_us(request):
    title = "About Us | TheVaultReviews"
    meta_description = "Learn more about The Vault Reviews, your go-to source for unbiased product reviews, expert opinions, and the latest deals on top-rated items."
    meta_keywords = "about The Vault Reviews, product review site, unbiased reviews, expert product opinions"

    return render(request, 'reviews/about_us.html', {
        'title': title,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
    })


def privacy_policy(request):
    title = "Privacy Policy | TheVaultReviews"
    meta_description = "Read our privacy policy to understand how The Vault Reviews collects, uses, and protects your personal information when you visit our website."
    meta_keywords = "privacy policy, data protection, personal information, The Vault Reviews"

    return render(request, 'reviews/privacy_policy.html', {
        'title': title,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
    })


def terms_conditions(request):
    title = "Terms & Conditions | TheVaultReviews"
    meta_description = "Review the terms and conditions of using The Vault Reviews, including legal agreements and your rights as a user."
    meta_keywords = "terms and conditions, user agreement, legal terms, The Vault Reviews"

    return render(request, 'reviews/terms_conditions.html', {
        'title': title,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
    })


def contact_us(request):
    title = "Contact Us | TheVaultReviews"
    meta_description = "Get in touch with The Vault Reviews for inquiries, feedback, or support regarding our product reviews and services."
    meta_keywords = "contact The Vault Reviews, customer support, inquiries, feedback"

    return render(request, 'reviews/contact_us.html', {
        'title': title,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
    })


def home(request):
    categories = Category.objects.all()
    return render(request, 'reviews/category_reviews.html', {'categories': categories})
