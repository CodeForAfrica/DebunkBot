import random
import logging
import tweepy
from django.conf import settings

from debunkbot.models import Reply, Claim, Tweet, Message
from debunkbot.twitter.selection import selector
from debunkbot.utils.gsheet.helper import GoogleSheetHelper
from debunkbot.twitter.api import create_connection


logger = logging.getLogger(__name__)

def update_sheet_with_response(tweet: Tweet) -> None:
    """Updates the gSheet with details pulled from the
    tweet we responded to
    """
    google_sheet = GoogleSheetHelper()
    value = google_sheet.get_cell_value(tweet.claim.sheet_row, int(settings.DEBUNKBOT_TWEETS_RESPONDED_COLUMN)) + \
        ', https://twitter.com/' + \
        tweet.tweet['user']['screen_name'] + \
        '/status/' + tweet.tweet['id_str']
    google_sheet.update_cell_value(tweet.claim.sheet_row, int(settings.DEBUNKBOT_TWEETS_RESPONDED_COLUMN), value)


def respond_to_tweet(tweet: Tweet) -> bool:
    """Responds to our selected tweet for the specific claim
    """
    api = create_connection()
    try:
        messages_count = Message.objects.count()
        if messages_count > 0:
            messages = Message.objects.all()
            message = messages[random.randint(0, messages_count-1)].message
        else:
            message = "We have checked this link and the news is false. "

        if tweet.claim.fact_checked_url:
                message += f" Check out this link {tweet.claim.fact_checked_url}"
        our_resp = api.update_status(
            f"Hello @{tweet.tweet.get('user').get('screen_name')} {message}.",
            tweet.tweet['id'])
    except tweepy.error.TweepError as error:
        print(f"The following error occurred {error}")
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
        Claim.objects.filter(id=tweet.claim_id).update(processed=True)
        Tweet.objects.filter(claim_id=tweet.claim_id).update(processed=True, responded=True)
