import validators
from celery.utils.log import get_task_logger

from debunkbot.celeryapp import app
from debunkbot.models import Claim, Tweet
from debunkbot.twitter.api import create_connection
from debunkbot.twitter.check_reply_impact import check_reply_impact
from debunkbot.twitter.check_tweets_metrics import check_tweets_metrics
from debunkbot.twitter.process_tweet import process_tweet
from debunkbot.twitter.search import search_claim_url, start_claims_search
from debunkbot.utils.claims_handler import fetch_claims_from_gsheet
from debunkbot.utils.gsheet import debunk_bot_gsheet_helper
from debunkbot.utils.gsheet.helper import GoogleSheetHelper

logger = get_task_logger(__name__)

api = create_connection()


@app.task(name="search_claims", task_ignore_result=True)
def search_claims():
    start_claims_search()


@app.task
def search_single_claim(url):
    if not validators.url(url):
        return
    tweet = search_claim_url(url, api)
    if tweet:
        claim = Claim.objects.filter(claim_first_appearance=url).first()
        create_tweet_in_db(tweet, claim)


def create_tweet_in_db(data, claim):
    tweet = Tweet.objects.create(tweet=data)
    tweet.claim = claim
    tweet.save()


@app.task(name="check_tweet_metrics", task_ignore_result=True)
def check_tweet_metrics():
    logger.info("Checking metrics of searched tweets...")
    tweets = Tweet.objects.filter(processed=False, deleted=False)
    logger.info(f"Checking Metrics of the following tweets\n {list(tweets)}")
    check_tweets_metrics(tweets)
    logger.info("Done checking Metrics")


@app.task(name="send_replies_task", task_ignore_result=True)
def send_replies_task():
    logger.info("Sending reply to one of the tweets with debunked info")
    process_tweet()
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
