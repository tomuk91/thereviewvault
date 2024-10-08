from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sites.models import Site
from django.conf import settings
from deals.models import Deal
from reviews.utils import post_to_twitter  # Import the function from utils.py
from django.db import transaction

@receiver(post_save, sender=Deal)
def post_deal_to_twitter(sender, instance, created, **kwargs):
    if created and not settings.DEBUG:  # Only post to Twitter when a new deal is created and not in DEBUG mode
        # Use a lambda to delay the post until after the database transaction is complete
        transaction.on_commit(lambda: handle_post_deal_to_twitter(instance, created))

def handle_post_deal_to_twitter(instance, created):
    message = f"New Deal!: {instance.title}!"
    tags = [tag.name for tag in instance.tags.all()[:4]]
    url = instance.link  # Use the 'link' field from the database

    # Assuming your image is saved locally or in a media folder
    image_path = instance.image.path if instance.image else None  # Get the image path if it exists

    post_to_twitter(message, tags=tags, url=url, image_path=image_path)
