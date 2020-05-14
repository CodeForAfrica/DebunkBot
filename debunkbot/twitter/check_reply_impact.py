import tweepy
from debunkbot.models import Tweet
from utils.gsheet.helper import GoogleSheetHelper
from utils.twitter.connection import create_connection

def check_reply_impact():
    api = create_connection()
    tweets = Tweet.objects.filter(responded=True)
    for tweet in tweets:
        retweet_count = 0
        likes_count = 0
        replies = []

        tweet_reply_author = tweet.reply_author
        reply_id = tweet.reply_id
        
        try:
            reply_impact = api.get_status(reply_id)
        except Exception as error:
            print("The tweet was deleted.")
            continue

        retweet_count = reply_impact._json.get('retweet_count')
        likes_count = reply_impact._json.get('favorite_count')
        
        interractions = tweepy.Cursor(api.search, q=f'to:{tweet_reply_author}', since_id=reply_id, max_id=None).items()
        for interraction in interractions:
            response = interraction._json
            usr_who_responded_to_our_response = response.get('user').get('screen_name')
            message = response.get('text')
            replies.append((usr_who_responded_to_our_response, message))
        
        tweet.impact = {'retweet_count': retweet_count, 
                        'likes_count': likes_count,
                        'replies_count': len(replies),
                        'replies': replies,
                        }
        tweet.save()
        google_sheet = GoogleSheetHelper()
        gsheet_update = ''
        for key, value in tweet.impact.items():
            gsheet_update += key + " = " +str(value) + '\n'
        google_sheet.update_cell_value(tweet.sheet_row, 12, gsheet_update)
