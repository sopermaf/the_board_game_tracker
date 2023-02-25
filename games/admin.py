from django.contrib import admin

from .forms import BoardGameForm, GameCategoryForm, PlayedBoardGameForm
from .models import BoardGame, BoardGameTag, PlayedBoardGame


@admin.register(PlayedBoardGame)
class PlayedBoardGameAdmin(admin.ModelAdmin):
    list_display = ["board_game", "played_by", "date_played"]
    search_fields = ["board_game__name"]
    list_filter = ["played_by"]
    list_per_page = 10
    form = PlayedBoardGameForm


@admin.register(BoardGame)
class BoardGameAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "game_weight",
        "range_of_players",
        "game_duration_mins",
        "price",
    ]
    list_per_page = 20
    search_fields = ["name"]
    form = BoardGameForm


@admin.register(BoardGameTag)
class GameCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    form = GameCategoryForm
