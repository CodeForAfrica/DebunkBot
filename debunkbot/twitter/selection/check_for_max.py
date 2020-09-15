from typing import List, Optional

from debunkbot.models import IgnoreListGsheet, RespondListGsheet, ResponseMode, Tweet
from debunkbot.utils.gsheet.helper import GoogleSheetHelper


def get_ignore_list() -> List:
    sheet = GoogleSheetHelper()
    gsheet_ignore_lists = IgnoreListGsheet.objects.all()
    ignore_list = []
    for gsheet_ignore_list in gsheet_ignore_lists:
        sheet_data = sheet.open_work_sheet(
            gsheet_ignore_list.sheet_id, gsheet_ignore_list.worksheet_name
        )
        for data in sheet_data:
            name = data.get(gsheet_ignore_list.column_name)
            if name:
                ignore_list.append(name)

    return ignore_list


def get_respond_to_list() -> List:
    sheet = GoogleSheetHelper()
    gsheet_respond_to_lists = RespondListGsheet.objects.all()
    respond_list = []
    for respond_to_list in gsheet_respond_to_lists:
        sheet_data = sheet.open_work_sheet(
            respond_to_list.sheet_id, respond_to_list.worksheet_name
        )
        for data in sheet_data:
            twitter_handle = data.get(respond_to_list.column_name)
            if twitter_handle:
                respond_list.append(twitter_handle.lower())
    return respond_list


def check_for_max(tweets: List[Tweet]) -> Optional[Tweet]:
    """Runs all related tweets through our little algorithm
    to determine which to select as the tweet we'll respond to
    """
    tweets_ = []  # type: List[Tweet]
    ignore_list = get_ignore_list()
    respond_to_list = []
    response_mode = ResponseMode.objects.first()
    if response_mode and response_mode.response_mode == "Response List":
        # Use the response list
        respond_to_list = get_respond_to_list()

    for tweet in tweets:
        if respond_to_list:
            # Only retain tweets that belong to accounts we should respond to.
            if tweet.tweet["user"]["screen_name"].lower() in respond_to_list:
                tweets_.append(tweet)
        else:
            # only retain tweets that
            # the accounts that tweeted them are not in our ignore list
            if tweet.tweet["user"]["screen_name"] not in ignore_list:
                tweets_.append(tweet)

    max_tweet = max(tweets_, key=lambda x: x.tweet["weight"])  # type: Tweet
    max_tweets = [
        tweet for tweet in tweets_ if tweet.tweet["weight"] == max_tweet.tweet["weight"]
    ]  # type: List[Tweet]
    if len(max_tweets) == 0:
        return None
    else:
        return sorted(max_tweets, key=lambda x: x.tweet["id"])[0]
