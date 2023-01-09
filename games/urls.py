from django.urls import path

from .views import BoardGameListView

app_name = "games"
urlpatterns = [
    path("", view=BoardGameListView.as_view(), name="list"),
]
