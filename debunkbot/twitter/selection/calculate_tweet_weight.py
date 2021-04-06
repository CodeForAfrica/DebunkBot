def calculate_tweet_weight(tweet: dict) -> int:
    """Calculates the weight for a specific tweet using
    our weight formula:
    weight =    (retweet_count * 4)     +
                (quote_count * 3)       +
                (replies_count * 3)     +
                (favorite_count * 3)    +
                (followers_count * 1)   +
                // if the user is verified, we assign 1 to verified, else 0
                (verified * 1)
    We assign specific multipliers to each metric based on
    how fast we think a tweet goes viral based on the metric
    """

    metrics_weight = {
        "retweet_count": 4,
        "quote_count": 3,
        "replies_count": 3,
        "favorite_count": 3,
        "verified": 1,
        "followers_count": 1,
    }
    tweet_weight = tweet.get("retweet_count", 0) * metrics_weight.get(
        "retweet_count", 0
    )  # type: int
    tweet_weight += tweet.get("quote_count", 0) * metrics_weight.get("quote_count", 0)
    tweet_weight += tweet.get("replies_count", 0) * metrics_weight.get(
        "replies_count", 0
    )
    tweet_weight += tweet.get("favorite_count", 0) * metrics_weight.get(
        "favorite_count", 0
    )
    tweet_weight += tweet.get("user", {}).get(
        "followers_count", 0
    ) * metrics_weight.get("followers_count", 0)
    tweet_weight += (
        metrics_weight.get("verified", 0)
        if tweet.get("user", {}).get("verified", False)
        else 0
    )
    return tweet_weight
