from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Review
from django.utils import timezone


class ReviewSitemap(Sitemap):
    changefreq = "daily"  # The frequency search engines should check for updates
    priority = 0.7  # Priority of the page, 0.0 to 1.0

    def items(self):
        return Review.objects.filter(publication_date__lte=timezone.now())


    def lastmod(self, obj):
        return obj.modified_date  # Date when the review was last modified

    def location(self, obj):
        return reverse('review_detail', args=[obj.slug])