import json

from django.views.generic import DetailView, ListView
from django_filters.views import FilterView

from the_board_game_tracker.users.models import User

from .filters import BoardGameFilter
from .models import BoardGame, PlayedBoardGame


class LeaderBoard(ListView):
    """Shows the top players with fewest remaining games"""

    template_name = "games/leaderboard.html"
    context_object_name = "users"

    def get_queryset(self):
        # NOTE: required here to avoid caching the board game total count
        return User.objects.leaderboard()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_newly_played"] = PlayedBoardGame.objects.newly_played_updates()
        context["hot_users"] = PlayedBoardGame.objects.leaders_of_recently_played(
            days_behind_window=30
        )
        data = PlayedBoardGame.objects.game_played_over_time_annotation()
        context["game_progress_chart_data"] = json.dumps(data, default=str)
        context["usernames"] = list(User.objects.values_list("username", flat=True))
        return context


class BoardGameListView(FilterView):
    model = BoardGame
    context_object_name = "games"
    filterset_class = BoardGameFilter
    paginate_by = 10
    queryset = BoardGame.objects.order_by_clean_name()


class BoardGameListTable(BoardGameListView):
    template_name = "games/boardgame_filter_table.html"


class BoardGameDetailView(DetailView):
    model = BoardGame
    slug_field = "name"
    slug_url_kwarg = "name"
    context_object_name = "game"
