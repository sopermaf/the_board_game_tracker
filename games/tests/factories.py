import datetime
import decimal

import factory
import factory.django

from games import models
from the_board_game_tracker.users.tests.factories import UserFactory


class BoardGameTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.BoardGameTag

    name = factory.Faker("company")


class BoardGameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.BoardGame
        django_get_or_create = ["name"]

    name = factory.Faker("name")
    game_weight = decimal.Decimal("2.5")
    range_of_players = (2, 4)
    game_duration_mins = (30, 45)
    price = decimal.Decimal("10")


class PlayedBoardGameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PlayedBoardGame

    played_by = factory.SubFactory(UserFactory)
    board_game = factory.SubFactory(BoardGameFactory)
    date_played = datetime.date(2020, 1, 1)


class UserWithGamePlayedFactory(UserFactory):
    game_played = factory.RelatedFactory(
        PlayedBoardGameFactory,
        factory_related_name="played_by",
    )


class UserWith2GamesPlayedFactory(UserFactory):
    game_played1 = factory.RelatedFactory(
        PlayedBoardGameFactory,
        factory_related_name="played_by",
        board_game__name="group1",
    )
    game_played2 = factory.RelatedFactory(
        PlayedBoardGameFactory,
        factory_related_name="played_by",
        board_game__name="group2",
    )
