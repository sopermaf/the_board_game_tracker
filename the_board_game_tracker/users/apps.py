import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "the_board_game_tracker.users"
    verbose_name = _("Users")

    def ready(self):
        with contextlib.suppress(ImportError):
            import the_board_game_tracker.users.signals  # noqa: F401
