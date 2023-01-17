from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Value
from django.db.models.functions import Lower, Replace
from django.forms import SelectMultiple
from django_filters import FilterSet, NumberFilter, RangeFilter
from django_filters.filters import ModelMultipleChoiceFilter
from psycopg2.extras import NumericRange

from .models import BoardGame, BoardGameTag

User = get_user_model()

multi_select = SelectMultiple(
    attrs={
        "class": "chosen-select expand",
        "data-placeholder": "begin typing...",
    }
)


class BoardGameFilter(FilterSet):
    not_played_by = ModelMultipleChoiceFilter(
        field_name="played_by",
        exclude=True,
        queryset=User.objects.order_by("username"),
        widget=multi_select,
    )
    tags = ModelMultipleChoiceFilter(
        field_name="tags",
        queryset=BoardGameTag.objects.all(),
        widget=multi_select,
        method="must_contain_all",
    )
    game_weight = RangeFilter()
    game_duration_mins = NumberFilter(method="int_within_range")
    range_of_players = NumberFilter(
        method="int_within_range", label="Number of Players"
    )

    class Meta:
        model = BoardGame
        fields = [
            "tags",
            "not_played_by",
        ]

    def int_within_range(self, queryset: QuerySet, name: str, value: int):
        return queryset.filter(**{f"{name}__contains": NumericRange(value, value + 1)})

    def must_contain_all(Self, qs: QuerySet, name: str, value: Any):
        for v in value:
            qs = qs.filter(**{f"{name}__in": [v]})
        return qs

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        qs = qs.annotate(
            name_without_the=Replace(Lower("name"), Value("the "), Value(""))
        )

        return qs.order_by("name_without_the", "name")
