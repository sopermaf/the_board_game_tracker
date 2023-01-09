from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple

from .models import BoardGame

User = get_user_model()


class BoardGameForm(ModelForm):
    class Meta:
        model = BoardGame
        fields = ["name", "played_by"]
        widgets = {"played_by": CheckboxSelectMultiple}
