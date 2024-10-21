from celery import shared_task
from django.contrib.sites.models import Site
from reviews.models import Review
from reviews.utils import post_to_twitter
from django.utils import timezone

@shared_task
def post_scheduled_review_to_twitter(review_id):
    review = Review.objects.get(id=review_id)

    if review.publication_date <= timezone.now():
        review.refresh_from_db()
        tags = [tag.name for tag in review.tags.all()[:4]]
        hashtags = ' '.join([f'#{tag}' for tag in tags])
        message = f"Latest Review: {review.title}"
        current_site = Site.objects.get_current()
        url = f"https://{current_site.domain}{review.get_absolute_url()}"

        image_path = review.image.path if review.image else None
        post_to_twitter(message, tags=tags, url=url, image_path=image_path, deal=False)
        
        # Reset task_scheduled after posting to Twitter (optional)
        review.task_scheduled = False
        review.save(update_fields=['task_scheduled'])


