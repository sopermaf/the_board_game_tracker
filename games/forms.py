from django.forms import ModelForm

from .models import BoardGame


class BoardGameForm(ModelForm):
    model = BoardGame
