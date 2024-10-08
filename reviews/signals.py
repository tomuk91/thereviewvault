# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sites.models import Site
from django.conf import settings
from reviews.models import Review
from deals.models import Deal
from reviews.utils import post_to_twitter  # Import the function from utils.py
from django.db import transaction

@receiver(post_save, sender=Review)
def post_review_to_twitter(sender, instance, created, **kwargs):
    if created and not settings.DEBUG:  # Only post to Twitter when a new review is created
        transaction.on_commit(lambda: handle_post_review_to_twitter(instance))

def handle_post_review_to_twitter(instance):
    # Reload the instance from the database to make sure the tags are properly loaded
    instance.refresh_from_db()
    tags = [tag.name for tag in instance.tags.all()[:4]]
    hashtags = ' '.join([f'#{tag}' for tag in tags])
    message = f"Latest Review: {instance.title}"
    current_site = Site.objects.get_current()
    url = f"https://{current_site.domain}{instance.get_absolute_url()}"

    # Assuming your image is saved locally or in a media folder
    image_path = instance.image.path if instance.image else None  # Get the image path

    post_to_twitter(message, tags=tags, url=url, image_path=image_path)



