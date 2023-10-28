import urllib.parse
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.postgres.aggregates import StringAgg
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Count, Value
from django.db.models.functions import Lower, Replace
from django.urls import reverse
from django.utils import timezone
from inclusive_django_range_fields import InclusiveIntegerRangeField

User = settings.AUTH_USER_MODEL


class ScrapingParseError(Exception):
    """Used for attempts to scrape websites that fail"""


class BoardGameTag(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class BoardGameManager(models.Manager):
    def order_by_clean_name(self):
        return self.annotate(
            name_without_the=Replace(Lower("name"), Value("the "), Value(""))
        ).order_by("name_without_the")


class BoardGame(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    date_added = models.DateField(default=timezone.now, blank=True, null=True)
    users_played_by = models.ManyToManyField(  # type: ignore
        User, related_name="games_played", through="PlayedBoardGame"
    )
    tags = models.ManyToManyField(BoardGameTag, related_name="games", blank=True)
    game_weight = models.DecimalField(
        decimal_places=2,
        max_digits=3,
        validators=[MaxValueValidator(5), MinValueValidator(1)],
    )
    range_of_players = InclusiveIntegerRangeField()
    game_duration_mins = InclusiveIntegerRangeField()
    price = models.DecimalField(
        default=0,
        decimal_places=2,
        max_digits=5,
        validators=[MinValueValidator(0)],
    )
    image_src = models.CharField(max_length=500, blank=True)
    board_game_geek_id = models.CharField(max_length=100, blank=True)

    objects = BoardGameManager()

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        # TODO: consider slug instead?
        return reverse("games:detail", kwargs={"name": self.name})

    @property
    def external_link(self):
        return f"https://boardgamegeek.com/{self.board_game_geek_id}"

    def scrape_boardgamegeek_img_src(self):
        """
        Scrapes image from board game geek and sets the `image_src` and `board_game_geek_ids`

        Raises HttpError if the request fails or ParseError for bad parsing results
        """
        # get the information from board game geek search page
        encoded_name = urllib.parse.quote(self.name)
        resp = requests.get(
            f"https://boardgamegeek.com/geeksearch.php?action=search&q={encoded_name}&objecttype=boardgame"
        )
        resp.raise_for_status()

        # parses the thumbnail as the first result from the search page
        soup = BeautifulSoup(resp.content, "html.parser")

        try:
            thumbnail_td = soup.find_all("td", class_="collection_thumbnail")[0]
            self.image_src = thumbnail_td.find_all("img")[0].attrs["src"]
            self.board_game_geek_id = thumbnail_td.find_all("a")[0].attrs["href"]
        except Exception:
            raise ScrapingParseError
        else:
            self.save()


class PlayedBoardGameManager(models.Manager):
    def newly_played_updates(self):
        return (
            self.values("date_played", "played_by__username")
            .annotate(
                games=StringAgg(
                    "board_game",
                    delimiter=", ",
                    ordering="board_game",
                )
            )
            .order_by("-date_played", "played_by__username")
            .filter(date_played__gte=date.today() - timedelta(days=30))
        )

    def leaders_of_recently_played(self, days_behind_window: int):
        return (
            self.filter(
                date_played__gte=date.today() - timedelta(days=days_behind_window)
            )
            .values("played_by__username")
            .annotate(total_played=Count("played_by__username"))
            .order_by("-total_played")
        )


class PlayedBoardGame(models.Model):
    played_by = models.ForeignKey(User, on_delete=models.CASCADE)
    board_game = models.ForeignKey(BoardGame, on_delete=models.CASCADE)
    date_played = models.DateField(default=timezone.now)

    objects = PlayedBoardGameManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("played_by", "board_game"), name="unique played instance"
            )
        ]
        ordering = ["-date_played", "board_game", "played_by"]

    def __str__(self) -> str:
        return f"{self.played_by}:{self.board_game}"
