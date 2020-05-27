import tweepy
from django.conf import settings

from debunkbot.models import Reply, Claim, Tweet
from debunkbot.twitter.selection import selector
from debunkbot.twitter.selection.mark_as_processed import mark_as_processed
from debunkbot.utils.gsheet.helper import GoogleSheetHelper
from debunkbot.twitter.api import create_connection


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
        our_resp = api.update_status(
            f"Hello @{tweet.tweet.get('user').get('screen_name')} We have checked this link and the news is false.",
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
        mark_as_processed(Claim.objects.filter(id=tweet.claim_id))
        mark_as_processed(Tweet.objects.filter(claim_id=tweet.claim_id))
