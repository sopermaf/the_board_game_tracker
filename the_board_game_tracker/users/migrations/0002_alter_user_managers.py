# Generated by Django 4.0.8 on 2023-02-24 21:11

from django.db import migrations
import the_board_game_tracker.users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', the_board_game_tracker.users.models.BoardGameUserManager()),
            ],
        ),
    ]
