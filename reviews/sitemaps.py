from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Review

class ReviewSitemap(Sitemap):
    changefreq = "weekly"  # The frequency search engines should check for updates
    priority = 0.8  # Priority of the page, 0.0 to 1.0

    def items(self):
        return Review.objects.all()  # Return all published reviews

    def lastmod(self, obj):
        return obj.modified_date  # Date when the review was last modified

    def location(self, obj):
        return reverse('review_detail', args=[obj.slug])