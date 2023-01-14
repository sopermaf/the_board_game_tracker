# Generated by Django 4.0.8 on 2023-01-14 12:20

import django.contrib.postgres.fields.ranges
import django.core.validators
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0007_auto_20230114_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boardgame',
            name='game_duration_mins',
        ),
        migrations.AlterField(
            model_name='boardgame',
            name='game_duration_range_mins',
            field=django.contrib.postgres.fields.ranges.IntegerRangeField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
