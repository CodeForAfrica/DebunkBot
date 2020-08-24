from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from django.conf import settings

from debunkbot.models import Tweet
from debunkbot.twitter.check_reply_impact import check_reply_impact
from debunkbot.twitter.check_tweets_metrics import check_tweets_metrics
from debunkbot.twitter.process_stream import process_stream
from debunkbot.twitter.stream_listener import stream
from debunkbot.utils.claims_handler import (
    extract_claims_from_posts,
    fetch_claims_from_gsheet,
    retrieve_claims_from_db,
)
from debunkbot.utils.gsheet import debunk_bot_gsheet_helper
from debunkbot.utils.gsheet.helper import GoogleSheetHelper
from debunkbot.utils.links_handler import get_links

logger = get_task_logger(__name__)

# The Intervals should be in minutes.
DEBUNKBOT_RESPONSE_INTERVAL = int(settings.DEBUNKBOT_RESPONSE_INTERVAL)
DEBUNKBOT_CHECK_TWEETS_METRICS_INTERVAL = int(
    settings.DEBUNKBOT_CHECK_TWEETS_METRICS_INTERVAL
)
DEBUNKBOT_CHECK_IMPACT_INTERVAL = int(settings.DEBUNKBOT_CHECK_IMPACT_INTERVAL)
DEBUNKBOT_BOT_FETCH_RESPONSES_MESSAGES_INTERVAL = int(
    settings.DEBUNKBOT_BOT_FETCH_RESPONSES_MESSAGES_INTERVAL
)
DEBUNKBOT_BOT_PULL_CLAIMS_INTERVAL = int(settings.DEBUNKBOT_BOT_PULL_CLAIMS_INTERVAL)
DEBUNKBOT_BOT_UPDATE_GSHEET_INTERVAL = int(
    settings.DEBUNKBOT_BOT_UPDATE_GSHEET_INTERVAL
)
DEBUNKBOT_RESTART_STREAM_LISTENER_INTERVAL = int(
    settings.DEBUNKBOT_RESTART_STREAM_LISTENER_INTERVAL
)


@periodic_task(
    run_every=(crontab(minute=f"*/{DEBUNKBOT_RESTART_STREAM_LISTENER_INTERVAL}")),
    name="track_claims_task",
    ignore_result=True,
)
def stream_listener():
    logger.info("Getting links to listen for...")
    claims = retrieve_claims_from_db()
    if claims:
        links = get_links(claims)
        logger.info(f"Got {len(links)} links.")
        logger.info("Starting stream listener...")
        stream(links)
    else:
        logger.info("No claims in the database.")


@periodic_task(
    run_every=(crontab(minute=f"*/{DEBUNKBOT_CHECK_TWEETS_METRICS_INTERVAL}")),
    name="check_tweet_metrics",
    ignore_result=True,
)
def check_tweet_metrics():
    logger.info("Checking metrics of streamed tweets...")
    tweets = Tweet.objects.filter(processed=False, deleted=False)
    logger.info(f"Checking Metrics of the following tweets\n {list(tweets)}")
    check_tweets_metrics(tweets)
    logger.info("Done checking Metrics")


@periodic_task(
    run_every=(crontab(minute=f"*/{DEBUNKBOT_RESPONSE_INTERVAL}")),
    name="send_replies_task",
    ignore_result=True,
)
def send_replies_task():
    logger.info("Sending reply to one of the tweets with debunked info")
    process_stream()
    logger.info("Done sending replies")


@periodic_task(
    run_every=(crontab(minute=f"*/{DEBUNKBOT_CHECK_IMPACT_INTERVAL}")),
    name="check_replies_impact",
    ignore_result=True,
)
def check_replies_impact():
    tweets = Tweet.objects.filter(responded=True)
    logger.info(
        f"Checking impact of our replies to the following tweets\n {list(tweets)}"
    )
    check_reply_impact()
    logger.info("Done checking Impact")


@periodic_task(
    run_every=(crontab(minute=f"*/{DEBUNKBOT_BOT_FETCH_RESPONSES_MESSAGES_INTERVAL}")),
    name="fetch_response_messages",
    ignore_result=True,
)
def fetch_bot_response_messages():
    logger.info("Fetching messages from google sheet...")
    gsheet_helper = GoogleSheetHelper()
    gsheet_helper.fetch_response_messages()
    logger.info("Done processing messages...")


@periodic_task(
    run_every=(crontab(minute=0, hour=f"*/{DEBUNKBOT_BOT_PULL_CLAIMS_INTERVAL}")),
    name="pull_claims_from_gsheet",
    ignore_result=True,
)
def pull_claims_from_gsheet():
    logger.info("Fetching claims from google sheets...")
    total_claims = fetch_claims_from_gsheet()
    logger.info(f"Fetched {total_claims} Claims")


@periodic_task(
    run_every=(crontab(minute=0, hour=f"*/{DEBUNKBOT_BOT_PULL_CLAIMS_INTERVAL}")),
    name="extract_claims_from_web_posts",
    ignore_result=True,
)
def extract_claims_from_web_posts():
    logger.info("Extracting Claims from website posts...")
    total_extracted_claims = extract_claims_from_posts()
    logger.info(f"Extracted {total_extracted_claims} Claims")


@periodic_task(
    run_every=(crontab(minute=f"*/{DEBUNKBOT_BOT_UPDATE_GSHEET_INTERVAL}")),
    name="update_debunkbot_google_sheet",
    ignore_result=True,
)
def update_debunkbot_google_sheet():
    logger.info("Updating debunkbot google sheet...")
    debunk_bot_gsheet_helper.update_debunkbot_gsheet()
    logger.info("Finished the Upadate.")
