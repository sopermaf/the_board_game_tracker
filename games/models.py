from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Value
from django.db.models.functions import Lower, Replace
from django.urls import reverse
from django.utils import timezone
from inclusive_django_range_fields import InclusiveIntegerRangeField

User = settings.AUTH_USER_MODEL


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
    users_played_by = models.ManyToManyField(
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

    objects = BoardGameManager()

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        # TODO: consider slug instead?
        return reverse("games:detail", kwargs={"name": self.name})


class PlayedBoardGame(models.Model):
    played_by = models.ForeignKey(User, on_delete=models.CASCADE)
    board_game = models.ForeignKey(BoardGame, on_delete=models.CASCADE)
    date_played = models.DateField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("played_by", "board_game"), name="unique played instance"
            )
        ]
        ordering = ["-date_played", "board_game", "played_by"]

    def __str__(self) -> str:
        return f"{self.played_by}:{self.board_game}"
