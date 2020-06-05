from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from django.conf import settings

from debunkbot.utils.gsheet.helper import GoogleSheetHelper
from debunkbot.twitter.stream_listener import stream
from debunkbot.models import Tweet
from debunkbot.twitter.process_stream import process_stream
from debunkbot.twitter.check_tweets_metrics import check_tweets_metrics
from debunkbot.twitter.check_reply_impact import check_reply_impact
from debunkbot.utils.links_handler import get_links

logger = get_task_logger(__name__)

# The Intervals should be in minutes.
DEBUNKBOT_RESPONSE_INTERVAL = int(settings.DEBUNKBOT_RESPONSE_INTERVAL)
DEBUNKBOT_REFRESH_TRACK_LIST_TIMEOUT = int(settings.DEBUNKBOT_REFRESH_TRACK_LIST_TIMEOUT)
DEBUNKBOT_CHECK_TWEETS_METRICS = int(settings.DEBUNKBOT_CHECK_TWEETS_METRICS)
DEBUNKBOT_CHECK_IMPACT_INTERVAL = int(settings.DEBUNKBOT_CHECK_IMPACT_INTERVAL)
DEBUNKBOT_BOT_FETCH_RESPONSES_MESSAGES_INTERVAL = int(settings.DEBUNKBOT_BOT_FETCH_RESPONSES_MESSAGES_INTERVAL)

@periodic_task(run_every=(crontab(minute=f'*/{DEBUNKBOT_REFRESH_TRACK_LIST_TIMEOUT}')), name="refresh_claims_list", ignore_result=True)
def refresh_claims_list():
    logger.info("Refreshing Claim List")
    gsheet_helper = GoogleSheetHelper()
    claims = gsheet_helper.get_claims()
    logger.info(f"Total Claims {len(claims)}")

@periodic_task(run_every=(crontab(minute=f'*/{DEBUNKBOT_REFRESH_TRACK_LIST_TIMEOUT}')), name="start_stream_listener_task", ignore_result=True)
def stream_listener():
    logger.info("Getting links to listen for...")
    gsheet_helper = GoogleSheetHelper()
    links = get_links(gsheet_helper)
    x = list(set(links))
    logger.info(f"Got {len(x)} links.")
    logger.info("Starting stream listener...")
    stream(x)

@periodic_task(run_every=(crontab(minute=f'*/{DEBUNKBOT_CHECK_TWEETS_METRICS}')), name="check_tweet_metrics", ignore_result=True)
def check_tweet_metrics():
    logger.info(f'Checking metrics of streamed tweets...')
    tweets = Tweet.objects.filter(processed=False, deleted=False)
    logger.info(f'Checking Metrics of the following tweets\n {list(tweets)}')
    check_tweets_metrics(tweets)
    logger.info(f'Done checking Metrics')
    
@periodic_task(run_every=(crontab(minute=f'*/{DEBUNKBOT_RESPONSE_INTERVAL}')), name="send_replies_task", ignore_result=True)
def send_replies_task():
    logger.info(f'Sending reply to one of the tweets with debunked info')
    process_stream()
    logger.info(f'Done sending replies')

@periodic_task(run_every=(crontab(minute=f'*/{DEBUNKBOT_CHECK_IMPACT_INTERVAL}')), name="check_replies_impact", ignore_result=True)
def check_replies_impact():
    tweets = Tweet.objects.filter(responded=True)
    logger.info(f'Checking impact of our replies to the following tweets\n {list(tweets)}')
    check_reply_impact()
    logger.info(f'Done checking Impact')

@periodic_task(run_every=(crontab(minute=f'*/{DEBUNKBOT_BOT_FETCH_RESPONSES_MESSAGES_INTERVAL}')), name="fetch_response_messages", ignore_result=True)
def fetch_bot_response_messages():
    logger.info(f'Fetching messages from google sheet...')
    gsheet_helper = GoogleSheetHelper()
    gsheet_helper.fetch_response_messages()
    logger.info(f'Done processing messages...')