from django.conf import settings

from debunkbot.models import Tweet, Reply
from debunkbot.utils.gsheet.helper import GoogleSheetHelper
from debunkbot.twitter.api import create_connection


def process_stream() -> None:
    api = create_connection()
    tweets = Tweet.objects.filter(processed=False)
    for t in tweets:
        print("Processing ----> ", t)
        if t.tweet['user']['followers_count'] > -1:
            try:
                our_resp = api.update_status(
                    f"Hello @{t.tweet.get('user').get('screen_name')} We have checked this link and the news is false.",
                    t.tweet['id'])
            except tweepy.error.TweepError as error:
                print(f"The following error occured {error}")
                continue
            reply_id = our_resp._json.get('id')
            reply_author = api.auth.get_username()
            reply = Reply.objects.create(reply_id=reply_id, reply_author=reply_author, tweet=t, reply=our_resp._json.get('text'))
            
            google_sheet = GoogleSheetHelper()
            value = google_sheet.get_cell_value(t.claim.sheet_row, int(settings.TWEETS_RESPONDED_COLUMN)) + ', https://twitter.com/' + \
                t.tweet['user']['screen_name'] + '/status/' + t.tweet['id_str']
            google_sheet.update_cell_value(t.claim.sheet_row, int(settings.TWEETS_RESPONDED_COLUMN), value)
            t.responded = True
        t.processed = True
        t.save()
