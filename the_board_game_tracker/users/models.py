from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import CharField, Count, Manager
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class LeaderBoardManager(Manager):
    def with_counts(self):
        from games.models import BoardGame

        total_board_games = BoardGame.objects.count()
        return self.annotate(
            number_unplayed_games=total_board_games - Count("games")
        ).order_by(
            "number_unplayed_games",
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

    objects = UserManager()
    leaderboard = LeaderBoardManager()

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
