from django.urls import path

from .views import BoardGameDetailView, BoardGameListTable, BoardGameListView

app_name = "games"
urlpatterns = [
    path("", view=BoardGameListView.as_view(), name="list"),
    path("table/", view=BoardGameListTable.as_view(), name="paged"),
    path("<str:name>", view=BoardGameDetailView.as_view(), name="detail"),
]
