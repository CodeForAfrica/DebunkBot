import tweepy
from debunkbot.models import Tweet
from utils.gsheet.helper import GoogleSheetHelper
from utils.twitter.connection import create_connection

def check_reply_impact():
    api = create_connection()
    tweets = Tweet.objects.filter(responded=True)
    for tweet in tweets:
        tweet_author = tweet.tweet.get('user').get('screen_name')
        reply_id = tweet.tweet.get('reply_id')
        interractions = tweepy.Cursor(api.search, q=f'to:{tweet_author}', since_id=reply_id).items()
        while True:
            try:
                interraction = interractions.next()
                response = interraction._json
                our_username = response.get('user').get('screen_name')
                # Update the impact
                tweet.impact = {'retweet_count': response.get('retweet_count'),
                                'favorite_count': response.get('favorite_count')}

                # Get replies to the tweet
                replies = tweepy.Cursor(api.search, q=f'to:{our_username}', since_id=reply_id).items()
                while True:
                    try:
                        reply = replies.next()
                        reply_json = reply._json
                        our_reply_responses = tweet.impact.get('response_replies', {})
                        our_reply_responses.update({reply_json.get('user').get('screen_name')+" At "+reply_json.get('created_at'): reply_json.get('text')})
                        tweet.impact.update({'response_replies': our_reply_responses})
                    except StopIteration:
                        break
                tweet.save()
                google_sheet = GoogleSheetHelper()
                gsheet_update = ''
                for key, value in tweet.impact.items():
                    gsheet_update += key + " = " +str(value) + '\n'
                google_sheet.update_cell_value(3, 12, gsheet_update)
            except StopIteration:
                break
