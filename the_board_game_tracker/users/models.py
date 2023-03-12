import enum
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import CharField, Count, DateField, F, Max, Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from games.models import BoardGame, PlayedBoardGame


class LeaderBoardStates(enum.Enum):
    HOT = "🔥", timedelta(days=14), False
    NORMAL = "", timedelta(days=28), True
    COLD = "🧊", timedelta(days=90), True
    DEAD = "💀", None, True

    def __init__(self, symbol, max_days_threshold, repeats_counted):
        self.symbol = symbol
        self.max_days_threshold = max_days_threshold
        self.repeats_counted = repeats_counted


class BoardGameUserManager(UserManager):
    def leaderboard(self):
        total_board_games = BoardGame.objects.count()
        qs = self.annotate(
            number_unplayed_games=total_board_games - Count("games_played")
        )
        qs = qs.annotate(
            completed_weight=Sum(Coalesce(F("games_played__game_weight"), Decimal(0)))
        )
        qs = qs.annotate(most_recent_game=Max("playedboardgame__date_played"))

        return qs.order_by("number_unplayed_games", "-most_recent_game", "username")


class User(AbstractUser):
    """
    Default custom user model for The Games List.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    # used to not punish players for replaying games
    # by marking them as `cold` or `dead`
    replayed_game_date = DateField(blank=True, null=True)

    objects = BoardGameUserManager()

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    @property
    def status(self):
        date_played = PlayedBoardGame.objects.filter(played_by=self)[:1][0].date_played
        new_game_played = date.today() - date_played

        for state in LeaderBoardStates:
            if (
                state.max_days_threshold is None
                or new_game_played < state.max_days_threshold
                or (
                    state.repeats_counted
                    and self.replayed_game_date
                    and date.today() - self.replayed_game_date
                    < state.max_days_threshold
                )
            ):
                return state

        raise ValueError("something went wrong")
