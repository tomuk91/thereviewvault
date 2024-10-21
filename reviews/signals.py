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
from django.db import transaction

@receiver(post_save, sender=Review)
def post_review_to_twitter(sender, instance, created, **kwargs):
    if created and not instance.task_scheduled and not settings.DEBUG:
        def schedule_task():
            if instance.publication_date > timezone.now():
                # Schedule the task to post the review on Twitter at the publication date
                post_scheduled_review_to_twitter.apply_async(kwargs={'review_id': instance.id, 'now': False}, eta=instance.publication_date)
            else:
                # If the publication date is in the past, post immediately
                post_scheduled_review_to_twitter.delay(instance.id, now=True)

            # Mark the task as scheduled to avoid duplication
            instance.task_scheduled = True
            instance.save(update_fields=['task_scheduled'])

        # Ensure the task is scheduled only after the review has been fully saved
        transaction.on_commit(schedule_task)


@receiver(post_save, sender=Review)
def post_review_to_indexnow(sender, instance, created, **kwargs):
    if created and not settings.DEBUG:  # Only submit to IndexNow if the review is newly created
        current_site = Site.objects.get_current()  # Get the current site domain dynamically
        review_url = f"https://{current_site.domain}{reverse('review_detail', args=[instance.slug])}"
        submit_to_indexnow(review_url)


