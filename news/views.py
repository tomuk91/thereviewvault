from django.shortcuts import render, get_object_or_404
from .models import NewsArticle, NewsCategory
from django.shortcuts import get_object_or_404, render
from .models import NewsArticle
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import NewsArticle, NewsCategory

def news_list(request):
    articles = NewsArticle.objects.all()
    categories = NewsCategory.objects.all()  # Retrieve all categories for display on the list page

    # Meta information for the news list page
    title = "News - The Vault Reviews"
    meta_description = "Read the latest news and updates on various topics."
    meta_tags = "news, updates, articles, latest news"

    # Set up pagination
    paginator = Paginator(articles, 7)  # Show 10 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/news_list.html', {
        'page_obj': page_obj,  # Pass the page object instead of articles
        'categories': categories,  # Pass categories to the template
        'title': title,
        'meta_description': meta_description,
        'meta_tags': meta_tags,
    })


def news_detail(request, slug):
    article = get_object_or_404(NewsArticle, slug=slug)

    # Meta information for individual news articles
    title = article.title + " - TheVaultReviews"
    meta_description = article.content[:147]  # Use the first 150 characters of content as a fallback
    meta_tags = f"news, {article.category.name if article.category else ''}, {article.author}, latest updates, {', '.join(set(tag.name for tag in article.tags.all()))}"
    
    # Corrected line: Use NewsArticle.objects to access the manager
    related_articles = NewsArticle.objects.exclude(slug=slug)[:3]

    return render(request, 'news/news_detail.html', {
        'title': title,
        'article': article,
        'meta_description': meta_description,
        'related_articles': related_articles,
        'meta_keywords': meta_tags,
    })


def news_by_category(request, slug):
    category = get_object_or_404(NewsCategory, slug=slug)
    articles = NewsArticle.objects.filter(category=category)

    # Meta information for category pages
    meta_description = f"Explore articles in the {category.name} category."
    meta_tags = f"{category.name}, news, articles"
    
    return render(request, 'news/news_by_category.html', {
        'category': category,
        'articles': articles,
        'meta_description': meta_description,
        'meta_tags': meta_tags,
    })
