from django.contrib.auth import get_user_model
from django.views.generic import DetailView, ListView
from django_filters.views import FilterView

from .filters import BoardGameFilter
from .models import BoardGame

User = get_user_model()


class LeaderBoard(ListView):
    """Shows the top players with fewest remaining games"""

    model = User
    queryset = User.leaderboard.with_counts().all()
    template_name = "games/leaderboard.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["board_game_count"] = BoardGame.objects.count()
        return context


class BoardGameListView(FilterView):
    model = BoardGame
    queryset = BoardGame.objects.all()
    context_object_name = "games"
    filterset_class = BoardGameFilter


class BoardGameDetailView(DetailView):
    model = BoardGame
    slug_field = "name"
    slug_url_kwarg = "name"
    context_object_name = "game"
