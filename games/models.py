from django.conf import settings
from django.db import models


class BoardGame(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    played_by = models.ManyToManyField(settings.AUTH_USER_MODEL)
