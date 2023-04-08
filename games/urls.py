from django.urls import path

from .views import (
    BoardGameDetailView,
    BoardGameListTable,
    BoardGameListView,
    PlayedGamesListView,
)

app_name = "games"
urlpatterns = [
    path("", view=BoardGameListView.as_view(), name="list"),
    path("table/", view=BoardGameListTable.as_view(), name="paged"),
    path(
        "newly_played/", view=PlayedGamesListView.as_view(), name="new-played-updates"
    ),
    path("game/<str:name>/", view=BoardGameDetailView.as_view(), name="detail"),
]
