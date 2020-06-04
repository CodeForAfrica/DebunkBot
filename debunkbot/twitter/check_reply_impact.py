import tweepy
from django.conf import settings
from debunkbot.models import Tweet, Impact
from debunkbot.utils.gsheet.helper import GoogleSheetHelper
from debunkbot.twitter.api import create_connection, get_tweet_status


def check_reply_impact():
    api = create_connection()
    tweets = Tweet.objects.filter(responded=True)
    for tweet in tweets:
        retweet_count = 0
        likes_count = 0
        replies = []
        response = dict()
        if not hasattr(tweet, 'reply'):
            continue
        tweet_reply_author = tweet.reply.reply_author
        reply_id = tweet.reply.reply_id
        
        tweet_status = get_tweet_status(api, tweet.tweet.get('id'))
        if not tweet_status:
            # The tweet has been deleted thus we should update the database
            tweet.deleted = True
            tweet.save()

        reply_impact = get_tweet_status(api, reply_id)

        if reply_impact:
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
            impact.data = response
            impact.tweet_deleted = tweet.deleted
            impact.save()

            google_sheet = GoogleSheetHelper()
            google_sheet.update_cell_value(tweet.claim.sheet_row, int(settings.DEBUNKBOT_GSHEET_LIKES_COLUMN), impact.likes_count)
            google_sheet.update_cell_value(tweet.claim.sheet_row, int(settings.DEBUNKBOT_GSHEET_RETWEETS_COLUMN), impact.retweet_count)
            google_sheet.update_cell_value(tweet.claim.sheet_row, int(settings.DEBUNKBOT_GSHEET_REPLIES_COUNT_COLUMN), impact.replies_count)
            google_sheet.update_cell_value(tweet.claim.sheet_row, int(settings.DEBUNKBOT_GSHEET_REPLIES_COLUMN), str(impact.replies))
            google_sheet.update_cell_value(tweet.claim.sheet_row, int(settings.DEBUNKBOT_GSHEET_TWEET_DELETED_COLUMN), 'Yes' if impact.tweet_deleted else "No")
