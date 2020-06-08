import random
import logging
import tweepy
from django.conf import settings

from debunkbot.models import Reply, Claim, Tweet, MessageTemplate
from debunkbot.twitter.selection import selector
from debunkbot.utils.gsheet.helper import GoogleSheetHelper
from debunkbot.twitter.api import create_connection


logger = logging.getLogger(__name__)

def update_sheet_with_response(tweet: Tweet) -> None:
    """Updates the gSheet with details pulled from the
    tweet we responded to
    """
    google_sheet = GoogleSheetHelper()
    value = google_sheet.get_cell_value(tweet.claim.sheet_row, int(settings.DEBUNKBOT_GSHEET_TWEETS_RESPONDED_COLUMN)) + \
        ', https://twitter.com/' + \
        tweet.tweet['user']['screen_name'] + \
        '/status/' + tweet.tweet['id_str']
    google_sheet.update_cell_value(tweet.claim.sheet_row, int(settings.DEBUNKBOT_GSHEET_TWEETS_RESPONDED_COLUMN), value)


def respond_to_tweet(tweet: Tweet) -> bool:
    """Responds to our selected tweet for the specific claim
    """
    api = create_connection()
    try:
        message_templates_count = MessageTemplate.objects.count()
        if message_templates_count > 0:
            message_templates = MessageTemplate.objects.all()
            message_template = message_templates[random.randint(0, message_templates_count-1)].message_template
        else:
            message_template = "Hey, do you know the link you shared is known to be false?"

        if tweet.claim.fact_checked_url:
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
    the operation both in the database and on the gSheet.
    """
    tweet = selector()
    if tweet and respond_to_tweet(tweet):
        update_sheet_with_response(tweet)
        claims_in_a_row = Claim.objects.filter(sheet_row=tweet.claim.sheet_row)
        claims_in_a_row.update(processed=True)
        Tweet.objects.filter(id=tweet.id).update(responded=True)
        Tweet.objects.filter(claim_id__in=claims_in_a_row).update(processed=True)
