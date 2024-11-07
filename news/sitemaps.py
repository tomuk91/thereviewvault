# news/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import NewsArticle

class NewsArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return NewsArticle.objects.all()

    def lastmod(self, obj):
        return obj.publication_date

    def location(self, obj):
        return reverse('news_detail', args=[obj.slug])
