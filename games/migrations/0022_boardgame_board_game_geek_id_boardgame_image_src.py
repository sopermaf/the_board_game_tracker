# Generated by Django 4.0.8 on 2023-03-24 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0021_alter_boardgame_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='boardgame',
            name='board_game_geek_id',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='boardgame',
            name='image_src',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
