import tweepy
from django.conf import settings
from debunkbot.models import Tweet
from debunkbot.twitter.api import create_connection, get_tweet_status


def check_tweet_impact():
    api = create_connection()
    tweets = Tweet.objects.filter(processed=False)
    for tweet in tweets:
        tweet_status = get_tweet_status(api, tweet.tweet.get('id'))
        if not tweet_status:
            continue
        tweet_data = tweet_status._json
        tweet.tweet=tweet_data
        tweet.save()
