from django.contrib.auth import get_user_model
from django.views.generic import ListView

from .models import BoardGame

User = get_user_model()


class LeaderBoard(ListView):
    """Shows the top players with fewest remaining games"""

    model = User
    queryset = User.leaderboard.with_counts().all()
    template_name = "games/home.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["board_game_count"] = BoardGame.objects.count()
        return context


class BoardGameListView(ListView):
    model = BoardGame
    queryset = BoardGame.objects.all()
    template_name = "games/board_game_list_view.html"
    context_object_name = "games"
