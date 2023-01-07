from django.contrib import admin

from .forms import BoardGameForm
from .models import BoardGame


@admin.register(BoardGame)
class BoardGameAdmin(admin.ModelAdmin):
    list_display = ["name"]
    form = BoardGameForm
