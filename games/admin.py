from django.contrib import admin

from .forms import BoardGameForm, GameCategoryForm
from .models import BoardGame, GameCategory


@admin.register(BoardGame)
class BoardGameAdmin(admin.ModelAdmin):
    list_display = ["name"]
    form = BoardGameForm


@admin.register(GameCategory)
class GameCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    form = GameCategoryForm
