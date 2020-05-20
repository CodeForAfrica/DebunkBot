from debunkbot.twitter.api import create_connection, get_tweet_status
from debunkbot.twitter.selection.calculate_tweet_weight import calculate_tweet_weight


def check_tweets_metrics(tweets):
    api = create_connection()
    for tweet in tweets:
        tweet_status = get_tweet_status(api, tweet.tweet.get('id'))
        if not tweet_status:
            tweet.deleted = True
            tweet.save()
            continue
        tweet_data = tweet_status._json
        tweet_data['weight'] = calculate_tweet_weight(tweet_data)
        tweet.tweet = tweet_data  # Update tweet with new data
        tweet.save()
