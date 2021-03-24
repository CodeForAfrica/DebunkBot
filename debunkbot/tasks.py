from celery.utils.log import get_task_logger

from debunkbot.celeryapp import app
from debunkbot.models import Tweet
from debunkbot.twitter.check_reply_impact import check_reply_impact
from debunkbot.twitter.check_tweets_metrics import check_tweets_metrics
from debunkbot.twitter.process_stream import process_stream
from debunkbot.utils.claims_handler import (
    fetch_claims_from_gsheet,
    get_claim_from_db,
    retrieve_claims_from_db,
)
from debunkbot.utils.gsheet import debunk_bot_gsheet_helper
from debunkbot.utils.gsheet.helper import GoogleSheetHelper
from debunkbot.utils.links_handler import get_links

logger = get_task_logger(__name__)


@app.task(name="stream_listener", task_ignore_result=True)
def stream_listener():
    logger.info("Getting links to listen for...")
    claims = retrieve_claims_from_db()
    if claims:
        links = get_links(claims)
        logger.info(f"Got {len(links)} links.")
        logger.info("Starting stream listener...")
        from debunkbot.twitter.stream_listener import stream

        stream(links)
    else:
        logger.info("No claims in the database.")


@app.task
def process_tweet(url, tweet):
    claim = get_claim_from_db(url)
    if claim:
        # This tweets belongs to this claim
        create_tweet_in_db(tweet, claim)


def create_tweet_in_db(data, claim):
    tweet = Tweet.objects.create(tweet=data)
    tweet.claim = claim
    tweet.save()


@app.task(name="check_tweet_metrics", task_ignore_result=True)
def check_tweet_metrics():
    logger.info("Checking metrics of streamed tweets...")
    tweets = Tweet.objects.filter(processed=False, deleted=False)
    logger.info(f"Checking Metrics of the following tweets\n {list(tweets)}")
    check_tweets_metrics(tweets)
    logger.info("Done checking Metrics")


@app.task(name="send_replies_task", task_ignore_result=True)
def send_replies_task():
    logger.info("Sending reply to one of the tweets with debunked info")
    process_stream()
    logger.info("Done sending replies")


@app.task(name="check_replies_impact", task_ignore_result=True)
def check_replies_impact():
    tweets = Tweet.objects.filter(responded=True)
    logger.info(
        f"Checking impact of our replies to the following tweets\n {list(tweets)}"
    )
    check_reply_impact()
    logger.info("Done checking Impact")


@app.task(name="fetch_response_messages", task_ignore_result=True)
def fetch_bot_response_messages():
    logger.info("Fetching messages from google sheet...")
    gsheet_helper = GoogleSheetHelper()
    gsheet_helper.fetch_response_messages()
    logger.info("Done processing messages...")


@app.task(name="pull_claims_from_gsheet", task_ignore_result=True)
def pull_claims_from_gsheet():
    logger.info("Fetching claims from google sheets...")
    total_claims = fetch_claims_from_gsheet()
    logger.info(f"Fetched {total_claims} Claims")


@app.task(name="update_debunkbot_google_sheet", task_ignore_result=True)
def update_debunkbot_google_sheet():
    logger.info("Updating debunkbot google sheet...")
    debunk_bot_gsheet_helper.update_debunkbot_gsheet()
    logger.info("Finished the Upadate.")
