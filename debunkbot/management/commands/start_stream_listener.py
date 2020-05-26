import time
import tweepy
from django.core.management.base import BaseCommand, CommandError

from debunkbot.utils.gsheet.helper import GoogleSheetHelper
from debunkbot.twitter.stream_listener import stream


class Command(BaseCommand):
    help = 'Management command that starts the stream listener'

    def handle(self, *args, **options):
        while True:
            claims = GoogleSheetHelper().get_claims()
            links = []
            for claim in claims:
                if claim.claim_first_appearance:
                    url_link = claim.claim_first_appearance
                    if  url_link != '' and not claim.rating:
                        if len(url_link) > 60:
                            url_link = url_link.split("www.")[-1]
                            links.append(url_link)
                            if len(url_link) > 60:
                                url_link = url_link.split("/")[1]
                                links.extend(url_link)
                        else:
                            links.append(url_link)
                elif claim.claim_phrase:
                    links.append(claim.claim_phrase)
                else:
                    # We don't have anything to tack on this claim
                    continue
        
            self.stdout.write(self.style.SUCCESS(f'Stream listener running..'))
            stream(links)
            time.sleep(2)
