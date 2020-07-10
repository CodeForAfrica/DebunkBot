import random
import logging
import tweepy
from django.conf import settings

from debunkbot.models import Reply, Claim, Tweet, MessageTemplate
from debunkbot.twitter.selection import selector
from debunkbot.twitter.api import create_connection


logger = logging.getLogger(__name__)

def respond_to_tweet(tweet: Tweet) -> bool:
    """Responds to our selected tweet for the specific claim
    """
    api = create_connection()
    try:
        message_templates = MessageTemplate.objects.filter(claim_database=tweet.claim.claim_db)
        message_templates_count = message_templates.count()
        if message_templates_count > 0:
            message_template = message_templates[random.randint(0, message_templates_count-1)].message_template
        else:
            message_template = "Hey, do you know the link you shared is known to be false?"

        if tweet.claim.fact_checked_url and tweet.claim.fact_checked_url != 'N/A':
                message_template += f" Check out this link {tweet.claim.fact_checked_url}"
        our_resp = api.update_status(
            f"Hello @{tweet.tweet.get('user').get('screen_name')} {message_template}.",
            tweet.tweet['id'])
    except tweepy.error.TweepError as error:
        logger.error(f"The following error occurred {error}")
        return False
    reply_id = our_resp._json.get('id')
    reply_author = api.auth.get_username()
    Reply.objects.create(
        reply_id=reply_id,
        reply_author=reply_author,
        tweet=tweet,
        reply=our_resp._json.get('text'),
        data=our_resp._json)
    return True


def process_stream() -> None:
    """Selects tweets to process, responds to them and updates
    the operation in the database.
    """
    tweet = selector()
    if tweet and respond_to_tweet(tweet):
        Claim.objects.filter(id=tweet.claim.id).update(processed=True)
        Tweet.objects.filter(id=tweet.id).update(responded=True)
        Tweet.objects.filter(claim_id=tweet.claim.id).update(processed=True)
