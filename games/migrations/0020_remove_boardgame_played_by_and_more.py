# Generated by Django 4.0.8 on 2023-02-26 00:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_managers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0019_alter_playedboardgame_date_played'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boardgame',
            name='played_by',
        ),
        migrations.AlterField(
            model_name='boardgame',
            name='users_played_by',
            field=models.ManyToManyField(related_name='games_played', through='games.PlayedBoardGame', to=settings.AUTH_USER_MODEL),
        ),
    ]
