# utils.py

import tweepy
from django.conf import settings
import requests
import logging
import requests


def post_to_twitter(message, tags=None, url=None, image_path=None, deal=False):
    """
    Post a message with an optional image to Twitter using Tweepy.
    """

    # Twitter API v1.1 authentication for media uploads
    auth = tweepy.OAuth1UserHandler(
        settings.TWITTER_API_KEY,
        settings.TWITTER_API_SECRET_KEY,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET,
    )
    api_v1 = tweepy.API(auth)

    # Twitter API v2 authentication for tweet posting
    client_v2 = tweepy.Client(
        bearer_token=settings.TWITTER_BEARER_TOKEN,
        consumer_key=settings.TWITTER_API_KEY,
        consumer_secret=settings.TWITTER_API_SECRET_KEY,
        access_token=settings.TWITTER_ACCESS_TOKEN,
        access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
    )

    # Upload the image using API v1.1
    media_id = None
    if image_path:
        try:
            media = api_v1.media_upload(image_path)
            media_id = media.media_id_string
        except tweepy.TweepError as e:
            print(f"Error uploading media to Twitter: {e}")

    # Prepare the tweet text
    hashtags = ' '.join([f'#{tag.replace(" ", "")}' for tag in tags[:4]]) if tags else ''
    if deal == True:
        tweet_text = f"⭐{message}! ⭐\n\nClick here to get it now: {url if url else ''}\n\n{hashtags}".strip()
    else:
        tweet_text = f"⭐{message}! ⭐\n\nRead our full review: {url if url else ''}\n\n{hashtags}".strip()


    # Ensure the tweet length doesn't exceed Twitter's character limit
    if len(tweet_text) > 300:
        tweet_text = tweet_text[:297] + '...'  # Truncate the message to fit

    try:
        # Post the tweet using API v2
        if media_id:
            response = client_v2.create_tweet(text=tweet_text, media_ids=[media_id])
        else:
            response = client_v2.create_tweet(text=tweet_text)
        print(f"Successfully posted to Twitter: {response}")
    except tweepy.TweepyException as e:
        print(f"Error posting to Twitter: {e}")


# Set up basic logging configuration (if not already configured elsewhere)
logging.basicConfig(level=logging.INFO)

# Get the logger for the current module
logger = logging.getLogger(__name__)

def submit_to_indexnow(url):
    # Your API key from IndexNow
    api_key = "a9522e169f464f8694f4ba8856128cca"
    
    # IndexNow endpoint
    indexnow_endpoint = f"https://api.indexnow.org/indexnow?url={url}&key={api_key}"
    
    # Send the request
    try:
        response = requests.post(indexnow_endpoint)  # Use POST instead of GET
        if response.status_code == 200:
            logger.info(f"Successfully submitted {url} to IndexNow.")
        else:
            logger.error(f"Failed to submit {url}. Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        logger.error(f"Error submitting {url}: {str(e)}")



