from django.conf import settings

from debunkbot.models import Claim, Impact
from debunkbot.utils.gsheet.helper import GoogleSheetHelper


def update_debunkbot_gsheet():
    debunk_bot_gsheet_id = settings.DEBUNKBOT_GSHEET_ID
    g_sheet_helper = GoogleSheetHelper()

    sheet = g_sheet_helper.get_sheet(debunk_bot_gsheet_id)

    update_values = []
    claims_values = []

    tweets_counter = 2
    claims_counter = 2

    for claim in Claim.objects.all():
        for tweet in claim.tweets.all():
            tweet_url = f"https://twitter.com/{tweet.tweet['user']['screen_name']}/status/{tweet.tweet['id_str']}"
            tweet_user = str(tweet.tweet.get("user"))

            if hasattr(tweet, "reply"):
                reply = tweet.reply
                update_values.append(
                    {
                        "range": f"D{tweets_counter}:K{tweets_counter}",
                        "values": [[tweet_url, tweet_user, reply.reply]],
                    }
                )

                impact = Impact.objects.filter(reply=tweet.reply).first()
                if impact:
                    update_values[-1]["values"][0].extend(
                        [
                            impact.likes_count,
                            impact.retweet_count,
                            impact.replies_count,
                            impact.replies,
                            impact.reply.tweet.deleted,
                        ]
                    )
                else:
                    update_values[-1]["values"][0].extend(
                        ["0", "0", "0", "[]", "UNKNOWN"]
                    )
            else:
                update_values.append(
                    {
                        "range": f"D{tweets_counter}:K{tweets_counter}",
                        "values": [
                            [
                                tweet_url,
                                tweet_user,
                                "N/A",
                                "0",
                                "0",
                                "0",
                                "[]",
                                "UNKNOWN",
                            ]
                        ],
                    }
                )
            tweets_counter += 1
        if claim.tweets.count() > 0:
            if hasattr(claim.claim_db, "gsheetclaimsdatabase"):
                claim_link = f"https://docs.google.com/spreadsheets/d/{claim.claim_db.gsheetclaimsdatabase.spreadsheetId}"
            else:
                claim_link = claim.claim_db.websiteclaimdatabase.url
            claims_values.append(
                {
                    "range": f"A{claims_counter}:C{claims_counter}",
                    "values": [[claim.claim_db.name, claim_link, claim.claim_reviewed]],
                }
            )
            claims_counter = tweets_counter
    sheet.sheet1.batch_update(update_values)
    sheet.sheet1.batch_update(claims_values)
