# Generated by Django 4.0.8 on 2023-01-14 20:54

from django.db import migrations
import inclusive_django_range_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0012_remove_boardgame_game_duration_range_mins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardgame',
            name='range_of_players',
            field=inclusive_django_range_fields.fields.InclusiveIntegerRangeField(null=True),
        ),
    ]