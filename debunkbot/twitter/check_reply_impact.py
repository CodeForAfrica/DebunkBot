import tweepy
from django.conf import settings
from debunkbot.models import Tweet, Impact
from debunkbot.utils.gsheet.helper import GoogleSheetHelper
from debunkbot.twitter.api import create_connection

def check_reply_impact():
    api = create_connection()
    tweets = Tweet.objects.filter(responded=True)
    for tweet in tweets:
        retweet_count = 0
        likes_count = 0
        replies = []
        tweet_reply_author = tweet.reply.reply_author
        reply_id = tweet.reply.reply_id
        
        try:
            reply_impact = api.get_status(reply_id)
        except Exception as error:
            print("The following error occured ", error)
            continue
        retweet_count = reply_impact._json.get('retweet_count')
        likes_count = reply_impact._json.get('favorite_count')
        
        interractions = tweepy.Cursor(api.search, q=f'to:{tweet_reply_author}', since_id=reply_id, max_id=None).items()    
        for interraction in interractions:
            response = interraction._json
            usr_who_responded_to_our_response = response.get('user').get('screen_name')
            message = response.get('text')
            replies.append((usr_who_responded_to_our_response, message))
        
        try:
            impact = Impact.objects.get(reply=tweet.reply)
        except Exception:
            impact = Impact(reply=tweet.reply)
        impact.likes_count = likes_count
        impact.replies_count = len(replies)
        impact.retweet_count = retweet_count
        impact.replies = replies
        impact.save()

        google_sheet = GoogleSheetHelper()
        replies_impacts = google_sheet.get_cell_value(tweet.claim.sheet_row, int(settings.IMPACT_COLUMN))
        gsheet_update = "likes_count=" + str(impact.likes_count) + " retweet_count= " +str(impact.retweet_count) + '\n'+"replies="+str(impact.replies)
        google_sheet.update_cell_value(tweet.claim.sheet_row, int(settings.IMPACT_COLUMN), gsheet_update)
