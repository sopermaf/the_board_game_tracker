# Generated by Django 4.0.8 on 2023-01-14 11:36

import django.contrib.postgres.fields.ranges
from django.db import migrations, models

from django.db.models import F, Func


class AgeRange(Func):
    function = 'numrange'

def migrate_custome_name(apps, schema_editor):
    boardgame = apps.get_model("games","BoardGame")
    for game in boardgame.objects.all():
        game.game_duration_range_mins = (0, game.game_duration_mins)
        game.save()


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_remove_boardgame_game_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardgame',
            name='game_duration_mins',
            field=models.IntegerField(),
        ),
         migrations.AddField(
            model_name='boardgame',
            name='game_duration_range_mins',
            field=django.contrib.postgres.fields.ranges.IntegerRangeField(null=True, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.RunPython(migrate_custome_name, migrations.RunPython.noop),
    ]
