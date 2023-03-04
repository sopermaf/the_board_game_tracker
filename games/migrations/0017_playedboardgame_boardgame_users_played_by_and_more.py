# Generated by Django 4.0.8 on 2023-02-20 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def copy_users_to_new_through_table(apps, schema_editor):
    BoardGame = apps.get_model("games","BoardGame")
    PlayedBoardGame = apps.get_model("games","PlayedBoardGame")
    for board_game in BoardGame.objects.all():
        for user in board_game.played_by.all():
            PlayedBoardGame.objects.create(
                played_by=user,
                board_game=board_game
            )


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0016_alter_boardgame_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayedBoardGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_played', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='boardgame',
            name='users_played_by',
            field=models.ManyToManyField(blank=True, related_name='games_played', through='games.PlayedBoardGame', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='playedboardgame',
            name='board_game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.boardgame'),
        ),
        migrations.AddField(
            model_name='playedboardgame',
            name='played_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='playedboardgame',
            constraint=models.UniqueConstraint(fields=('played_by', 'board_game'), name='unique played instance'),
        ),
        migrations.RunPython(copy_users_to_new_through_table, migrations.RunPython.noop),
    ]