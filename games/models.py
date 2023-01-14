from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import IntegerRangeField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

User = get_user_model()


class BoardGameTag(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class BoardGame(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    played_by = models.ManyToManyField(User, related_name="games", blank=True)
    tags = models.ManyToManyField(BoardGameTag, related_name="games", blank=True)
    game_weight = models.DecimalField(
        decimal_places=2,
        max_digits=3,
        validators=[MaxValueValidator(5), MinValueValidator(1)],
    )
    range_of_players = IntegerRangeField()
    game_duration_range_mins = IntegerRangeField(validators=[MinValueValidator(0)])

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        # TODO: consider slug instead?
        return reverse("game:detail", kwargs={"name": self.name})
