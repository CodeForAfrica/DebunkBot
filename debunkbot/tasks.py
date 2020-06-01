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

logger = get_task_logger(__name__)

DEBUNKBOT_RESPONSE_INTERVAL = int(settings.DEBUNKBOT_RESPONSE_INTERVAL)//60
DEBUNKBOT_REFRESH_TRACK_LIST_TIMEOUT = (int(settings.DEBUNKBOT_REFRESH_TRACK_LIST_TIMEOUT)+5)//60
DEBUNKBOT_CHECK_TWEETS_METRICS = int(settings.DEBUNKBOT_CHECK_TWEETS_METRICS)//60
DEBUNKBOT_CHECK_IMPACT = int(settings.DEBUNKBOT_CHECK_IMPACT)//60

if DEBUNKBOT_RESPONSE_INTERVAL == 0:
    DEBUNKBOT_RESPONSE_INTERVAL = 1
if DEBUNKBOT_REFRESH_TRACK_LIST_TIMEOUT == 0:
    DEBUNKBOT_RESPONSE_INTERVAL = 1
if DEBUNKBOT_CHECK_TWEETS_METRICS == 0:
    DEBUNKBOT_CHECK_TWEETS_METRICS = 1
if DEBUNKBOT_CHECK_IMPACT == 0:
    DEBUNKBOT_CHECK_IMPACT = 1

@periodic_task(run_every=(crontab(minute=f'*/{DEBUNKBOT_REFRESH_TRACK_LIST_TIMEOUT}')), name="start_stream_listener_task", ignore_result=True)
def stream_listener():
    logger.info("Starting stream listener...")

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

@periodic_task(run_every=(crontab(minute=f'*/{DEBUNKBOT_CHECK_IMPACT}')), name="check_replies_impact", ignore_result=True)
def check_replies_impact():
    tweets = Tweet.objects.filter(responded=True)
    logger.info(f'Checking impact of our replies to the following tweets\n {list(tweets)}')
    check_reply_impact()
    logger.info(f'Done checking Impact')
