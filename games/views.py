from django.contrib.auth import get_user_model
from django.db.models import Count, QuerySet
from django.views.generic import DetailView, ListView
from django_filters.views import FilterView

from .filters import BoardGameFilter
from .models import BoardGame

User = get_user_model()


class LeaderBoard(ListView):
    """Shows the top players with fewest remaining games"""

    model = User
    template_name = "games/leaderboard.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_count"] = User.objects.count()
        return context

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        total_board_games = BoardGame.objects.count()
        qs = qs.annotate(number_unplayed_games=total_board_games - Count("games"))
        qs = qs.order_by("number_unplayed_games", "username")
        return qs[:10]


class BoardGameListView(FilterView):
    model = BoardGame
    context_object_name = "games"
    filterset_class = BoardGameFilter
    paginate_by = 10
    queryset = BoardGame.objects.order_by_clean_name()


class BoardGameDetailView(DetailView):
    model = BoardGame
    slug_field = "name"
    slug_url_kwarg = "name"
    context_object_name = "game"
