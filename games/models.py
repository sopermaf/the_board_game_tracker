from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class GameCategory(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    class Meta:
        verbose_name_plural = "game categories"

    def __str__(self) -> str:
        return self.name


class BoardGame(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    played_by = models.ManyToManyField(User, related_name="games", blank=True)
    category = models.ManyToManyField(GameCategory, related_name="games", blank=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        # TODO: consider slug instead?
        return reverse("game:detail", kwargs={"name": self.name})
