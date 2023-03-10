# Generated by Django 4.0.8 on 2023-01-14 12:52

from django.db import migrations
from django.db import migrations

from django.db.models import Func


class AgeRange(Func):
    function = 'numrange'

def migrate_custome_name(apps, schema_editor):
    boardgame = apps.get_model("games","BoardGame")
    for game in boardgame.objects.all():
        game.game_duration_mins = (game.game_duration_range_mins.lower, game.game_duration_range_mins.upper)
        game.save()

class Migration(migrations.Migration):

    dependencies = [
        ('games', '0010_boardgame_game_duration_mins'),
    ]

    operations = [
        migrations.RunPython(migrate_custome_name, migrations.RunPython.noop),
    ]
