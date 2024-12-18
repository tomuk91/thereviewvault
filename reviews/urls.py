from django.urls import path
from . import views
from .views import compare_reviews_view, privacy_policy, review_overview
from django.contrib.sitemaps.views import sitemap
from .sitemaps import ReviewSitemap
from news.sitemaps import NewsArticleSitemap
from .views import robots_txt

# Define sitemaps for different sections
sitemaps = {
    'reviews': ReviewSitemap,
}

news_sitemaps = {
    'news': NewsArticleSitemap,
}

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('review/<slug:slug>/', views.review_detail, name='review_detail'),
    path('category/<slug:slug>/', views.category_reviews, name='category_reviews'),
    path('search/', views.search_reviews, name='search_reviews'),
    path('tag/<slug:tag_slug>/', views.tagged_reviews, name='tagged_reviews'),
    path('reviews/rating/<str:rating>/', views.reviews_by_rating, name='reviews_by_rating'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('about/', views.about_us, name='about_us'),
    path('terms/', views.terms_conditions, name='terms_conditions'),
    path('contact/', views.contact_us, name='contact_us'),
    # Main sitemap including reviews (and optionally other sitemaps)
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # Dedicated sitemap for news articles only
    path('news-sitemap.xml', sitemap, {'sitemaps': news_sitemaps}, name='news-sitemap'),
    path("robots.txt", robots_txt, name="robots_txt"),
    path('callback/', views.twitter_callback, name='twitter_callback'),
    path('indexnow-key.txt', views.indexnow_key, name='indexnow_key'),
    path('hot-reviews', views.hot_reviews, name='hot_reviews'),
    path('archive/', views.review_archive, name='archive'),
    path('archive/<int:year>/<str:month>/', views.archive_by_month, name='archive_by_month'),
    path('reviews/', review_overview, name='review_overview'),
    path('compare-reviews/', compare_reviews_view, name='compare_reviews'),
    path('reviews/search/', views.search_reviews_for_compare, name='search_reviews_for_compare'),
]
