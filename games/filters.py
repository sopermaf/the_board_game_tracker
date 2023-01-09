from django_filters import FilterSet

from .models import BoardGame


class BoardGameFilter(FilterSet):
    class Meta:
        model = BoardGame
        fields = ["played_by", "category"]
