from django.contrib import admin

from .forms import BoardGameForm, GameCategoryForm
from .models import BoardGame, BoardGameTag


@admin.register(BoardGame)
class BoardGameAdmin(admin.ModelAdmin):
    list_display = ["name"]
    form = BoardGameForm


@admin.register(BoardGameTag)
class GameCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    form = GameCategoryForm
