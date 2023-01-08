from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BoardGame(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    played_by = models.ManyToManyField(User, related_name="games")

    def __str__(self) -> str:
        return self.name
