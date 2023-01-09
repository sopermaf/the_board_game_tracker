from django.urls import path

from .views import BoardGameDetailView, BoardGameListView

app_name = "games"
urlpatterns = [
    path("", view=BoardGameListView.as_view(), name="list"),
    path("<str:name>", view=BoardGameDetailView.as_view(), name="detail"),
]
