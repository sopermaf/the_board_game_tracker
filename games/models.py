from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class GameCategory(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    class Meta:
        verbose_name_plural = "game categories"

    def __str__(self) -> str:
        return self.name


class BoardGame(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    played_by = models.ManyToManyField(User, related_name="games")
    category = models.ManyToManyField(GameCategory, related_name="games")

    def __str__(self) -> str:
        return self.name
