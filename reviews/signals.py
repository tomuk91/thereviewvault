# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sites.models import Site
from django.conf import settings
from reviews.models import Review
from deals.models import Deal
from reviews.utils import post_to_twitter  # Import the function from utils.py
from django.db import transaction
from .utils import submit_to_indexnow
from django.urls import reverse
from .tasks import post_scheduled_review_to_twitter
from django.utils import timezone

@receiver(post_save, sender=Review)
def post_review_to_twitter(sender, instance, created, **kwargs):
    if created:
        # Schedule the task to post the review on Twitter at the publication date
        if instance.publication_date > timezone.now():
            post_scheduled_review_to_twitter.apply_async(kwargs={'review_id': instance.id}, eta=instance.publication_date)
        else:
            # If the publication date is in the past, post immediately
            post_scheduled_review_to_twitter.delay(instance.id)

# def handle_post_review_to_twitter(instance):
#     # Reload the instance from the database to make sure the tags are properly loaded
#     instance.refresh_from_db()
#     tags = [tag.name for tag in instance.tags.all()[:4]]
#     hashtags = ' '.join([f'#{tag}' for tag in tags])
#     message = f"Latest Review: {instance.title}"
#     current_site = Site.objects.get_current()
#     url = f"https://{current_site.domain}{instance.get_absolute_url()}"

#     # Assuming your image is saved locally or in a media folder
#     image_path = instance.image.path if instance.image else None  # Get the image path

#     post_to_twitter(message, tags=tags, url=url, image_path=image_path, deal=False)
    
@receiver(post_save, sender=Review)
def post_review_to_indexnow(sender, instance, created, **kwargs):
    if created and not settings.DEBUG:  # Only submit to IndexNow if the review is newly created
        current_site = Site.objects.get_current()  # Get the current site domain dynamically
        review_url = f"https://{current_site.domain}{reverse('review_detail', args=[instance.slug])}"
        submit_to_indexnow(review_url)


