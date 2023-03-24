import time

import requests.exceptions
from django.core.management.base import BaseCommand

from games.models import BoardGame, ScrapingParseError


class Command(BaseCommand):
    help = "Scrapes images from boardgamegeek if possible"

    def handle(self, *args, **options):
        qs = BoardGame.objects.filter(image_src="")
        for board_game in qs:
            self._handle_game(board_game)

    def _handle_game(self, board_game: BoardGame):
        try:
            board_game.scrape_boardgamegeek_img_src()
        except requests.exceptions.HTTPError:
            self.stdout.write(
                self.style.ERROR("request error %s. Sleeping..." % board_game.name)
            )
            time.sleep(30)
        except ScrapingParseError:
            self.stdout.write(
                self.style.ERROR('Failed to parse image "%s"' % board_game.name)
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Successfully found image "%s"' % board_game.name)
            )
            # minor delay magic number to avoid rate limiting
            time.sleep(0.3)
