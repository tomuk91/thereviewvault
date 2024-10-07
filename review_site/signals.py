# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sites.models import Site
from django.conf import settings
from reviews.models import Review
from deals.models import Deal
from reviews.utils import post_to_twitter  # Import the function from utils.py

@receiver(post_save, sender=Deal)
def post_deal_to_twitter(sender, instance, created, **kwargs):
    if created and not settings.DEBUG:  # Only post if the deal is newly created and not in DEBUG mode
        title = instance.title
        tags = [tag.name for tag in instance.tags.all()]
        url = instance.link  # Use the 'link' field from the database
        post_to_twitter(title, tags, url=url)  # Pass the title, tags, and URL to the utility function

@receiver(post_save, sender=Review)
def post_review_to_twitter(sender, instance, created, **kwargs):
    if created and not settings.DEBUG:  # Only post to Twitter if not in debug mode
        current_site = Site.objects.get_current()
        review_url = f"https://{current_site.domain}{instance.get_absolute_url()}"
        title = instance.title
        tags = [tag.name for tag in instance.tags.all()[:2]]  # Get the first two tags
        post_to_twitter(title, tags, url=review_url)  # Pass the title, tags, and review URL to the function
