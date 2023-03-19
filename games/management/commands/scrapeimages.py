import time

import requests.exceptions
from django.core.management.base import BaseCommand

from games.models import BoardGame, ScrapingParseError


class Command(BaseCommand):
    help = "Scrapes images from boardgamegeek if possible"

    def handle(self, *args, **options):
        qs = BoardGame.objects.filter(image_src__isnull=True)
        for board_game in qs:
            try:
                board_game.scrape_boardgamegeek_img_src()
            except requests.exceptions.HTTPError:
                self.stdout.write(
                    self.style.ERROR("request error %s. Sleeping..." % board_game.name)
                )
                time.sleep(5)
            except ScrapingParseError:
                self.stdout.write(
                    self.style.ERROR('Failed to parse image "%s"' % board_game.name)
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        'Successfully found image "%s"' % board_game.name
                    )
                )
