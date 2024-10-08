# utils.py

import tweepy
from django.conf import settings

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
    hashtags = ' '.join([f'#{tag}' for tag in tags[:4]]) if tags else ''
    if deal == True:
        tweet_text = f"⭐{message}! ⭐\nClick here to get it now: {url if url else ''}\n{hashtags}".strip()
    else:
        tweet_text = f"⭐{message}! ⭐\nRead our full review: {url if url else ''}\n{hashtags}".strip()


    # Ensure the tweet length doesn't exceed Twitter's character limit
    if len(tweet_text) > 280:
        tweet_text = tweet_text[:277] + '...'  # Truncate the message to fit

    try:
        # Post the tweet using API v2
        if media_id:
            response = client_v2.create_tweet(text=tweet_text, media_ids=[media_id])
        else:
            response = client_v2.create_tweet(text=tweet_text)
        print(f"Successfully posted to Twitter: {response}")
    except tweepy.TweepyException as e:
        print(f"Error posting to Twitter: {e}")
