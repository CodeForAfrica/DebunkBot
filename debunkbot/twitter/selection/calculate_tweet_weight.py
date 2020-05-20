def calculate_tweet_weight(tweet):
    metrics_weight = {
        'retweet_count': 4,
        'quote_count': 3,
        'replies_count': 3,
        'favorite_count': 3,
        'verified': 1,
        'followers_count': 1,
    }
    tweet_weight = tweet.get('retweet_count', 0) * metrics_weight.get('retweet_count', 0)
    tweet_weight += tweet.get('quote_count', 0) * metrics_weight.get('quote_count', 0)
    tweet_weight += tweet.get('replies_count', 0) * metrics_weight.get('replies_count', 0)
    tweet_weight += tweet.get('favorite_count', 0) * metrics_weight.get('favorite_count', 0)
    tweet_weight += tweet.get('user').get('followers_count', 0) * metrics_weight.get('followers_count', 0)
    tweet_weight += metrics_weight.get('verified', 0) if tweet.get('user').get('verified', False) else 0
    return tweet_weight
