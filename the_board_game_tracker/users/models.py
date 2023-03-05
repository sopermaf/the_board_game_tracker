from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import CharField, Count, DateField, Exists, F, Max, OuterRef, Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from games.models import BoardGame, PlayedBoardGame

_COLD_DAYS = 28
_DEAD_DAYS = 90


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

        qs = qs.annotate(
            is_hot=Exists(self._has_played_within(days_ago=14)),
            is_cold=~Exists(self._has_played_within(days_ago=_COLD_DAYS)),
            is_dead=~Exists(self._has_played_within(days_ago=_DEAD_DAYS)),
        )
        return qs.order_by("number_unplayed_games", "-most_recent_game", "username")

    def _has_played_within(self, days_ago: int) -> date:
        return PlayedBoardGame.objects.filter(
            played_by=OuterRef("pk"),
            date_played__gte=timezone.now() - timedelta(days=days_ago),
        )


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

    def has_not_replayed_recently(self) -> bool:
        threshold_date = timezone.now().date() - timedelta(days=_COLD_DAYS)
        return not self.replayed_game_date or self.replayed_game_date < threshold_date
