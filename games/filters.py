from django.contrib.auth import get_user_model
from django.forms import CheckboxSelectMultiple
from django_filters import FilterSet
from django_filters.filters import ModelMultipleChoiceFilter

from .models import BoardGame, GameCategory

User = get_user_model()


class BoardGameFilter(FilterSet):
    # not_played_by = ModelChoiceFilter(choices=, )
    not_played_by = ModelMultipleChoiceFilter(
        field_name="played_by",
        exclude=True,
        queryset=User.objects.all(),
        widget=CheckboxSelectMultiple,
    )
    category = ModelMultipleChoiceFilter(
        field_name="category",
        queryset=GameCategory.objects.all(),
        widget=CheckboxSelectMultiple,
    )

    class Meta:
        model = BoardGame
        fields = ["category", "not_played_by"]
