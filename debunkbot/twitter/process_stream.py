from debunkbot.models import Tweet
from debunkbot.utils.gsheet.helper import GoogleSheetHelper
from debunkbot.twitter.api import create_connection


def process_stream() -> None:
    api = create_connection()
    tweets = Tweet.objects.filter(processed=False)
    for t in tweets:
        if t.tweet['user']['followers_count'] > 100:
            api.update_status(
                "Hello! We have checked this link and the news is false",
                t.tweet['id'])
            google_sheet = GoogleSheetHelper()
            value = google_sheet.get_cell_value(2, 11) + ', https://twitter.com/' + \
                t.tweet['user']['screen_name'] + '/status/' + t.tweet['id_str']
            google_sheet.update_cell_value(2, 11, value)
            t.responded = True
        t.processed = True
        t.save()
