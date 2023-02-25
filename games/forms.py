from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

from .models import BoardGame, BoardGameTag, PlayedBoardGame

User = get_user_model()


class BoardGameForm(ModelForm):
    class Meta:
        model = BoardGame
        fields = [
            "name",
            "tags",
            "game_weight",
            "range_of_players",
            "game_duration_mins",
            "price",
        ]
        widgets = {
            "tags": CheckboxSelectMultiple,
        }


class GameCategoryForm(ModelForm):
    class Meta:
        model = BoardGameTag
        fields = ["name"]


class PlayedBoardGameForm(ModelForm):
    class Meta:
        model = PlayedBoardGame
        fields = ["board_game", "played_by", "date_played"]
