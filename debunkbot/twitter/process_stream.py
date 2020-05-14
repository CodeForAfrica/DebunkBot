from debunkbot.models import Tweet
from debunkbot.utils.gsheet.helper import GoogleSheetHelper
from debunkbot.twitter.api import create_connection


def process_stream() -> None:
    api = create_connection()
    tweets = Tweet.objects.filter(responded=False)
    for t in tweets:
        print("Processing ----> ", t)
        if t.tweet['user']['followers_count'] > -1:
            our_resp = api.update_status(
                f"Hello @{t.tweet.get('user').get('screen_name')} We have checked this link and the info is false",
                t.tweet['id'])
            t.reply_id = our_resp._json.get('id')
            t.reply_author = api.auth.get_username()
            google_sheet = GoogleSheetHelper()
            value = google_sheet.get_cell_value(t.sheet_row, 11) + ', https://twitter.com/' + \
                t.tweet['user']['screen_name'] + '/status/' + t.tweet['id_str']
            google_sheet.update_cell_value(t.sheet_row, 11, value)
            t.responded = True
        t.processed = True
        t.save()
