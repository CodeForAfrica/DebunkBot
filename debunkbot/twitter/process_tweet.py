import logging
import random

import tweepy

from debunkbot.models import Claim, MessageTemplate, Reply, ResponseMode, Tweet
from debunkbot.twitter.api import create_connection
from debunkbot.twitter.selection import selector

logger = logging.getLogger(__name__)


def respond_to_tweet(tweet: Tweet) -> bool:
    """Responds to our selected tweet for the specific claim"""
    api = create_connection()
    try:
        message_templates = MessageTemplate.objects.filter(
            message_template_category__iexact=tweet.claim.category
        )
        message_templates_count = message_templates.count()
        if message_templates_count > 0:
            message_template = message_templates[
                random.randint(0, message_templates_count - 1)
            ].message_template
        else:
            message_template = (
                "Hey, do you know the link you shared is known to be false?"
            )
        if tweet.claim.fact_checked_url and tweet.claim.fact_checked_url != "N/A":
            message_template += f" Check out this link {tweet.claim.fact_checked_url}"

        tweet_to_respond_to = tweet.tweet.get("retweeted_status") or tweet.tweet
        user_to_respond_to = tweet_to_respond_to.get("user").get("screen_name")
        tweet_id = tweet_to_respond_to.get("id")

        our_resp = api.update_status(
            f"Hello @{user_to_respond_to} {message_template}.",
            tweet_id,
        )
    except tweepy.error.TweepError as error:
        logger.error(f"The following error occurred {error}")
        return False
    reply_id = our_resp._json.get("id")
    reply_author = api.auth.get_username()
    Reply.objects.create(
        reply_id=reply_id,
        reply_author=reply_author,
        tweet=tweet,
        reply=our_resp._json.get("text"),
        data=our_resp._json,
    )
    return True


def process_tweet() -> None:
    """Selects a tweet to process, respond to it and update
    the operation in the database.
    """
    response_mode = ResponseMode.objects.first()
    if not response_mode or response_mode.response_mode == "No Responses":
        # We should not send any response
        return
    tweet = selector()
    if tweet and respond_to_tweet(tweet):
        Claim.objects.filter(id=tweet.claim.id).update(processed=True)
        Tweet.objects.filter(id=tweet.id).update(responded=True)
        Tweet.objects.filter(claim_id=tweet.claim.id).update(processed=True)
