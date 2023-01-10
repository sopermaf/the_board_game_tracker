from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

from .models import BoardGame, BoardGameTag

User = get_user_model()


class BoardGameForm(ModelForm):
    class Meta:
        model = BoardGame
        fields = [
            "name",
            "played_by",
            "tags",
            "game_weight",
            "range_of_players",
            "game_duration_mins",
        ]
        widgets = {
            "played_by": CheckboxSelectMultiple,
            "tags": CheckboxSelectMultiple,
        }


class GameCategoryForm(ModelForm):
    class Meta:
        model = BoardGameTag
        fields = ["name"]
