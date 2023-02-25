import datetime

import pytest
from freezegun import freeze_time

from games import models
from games.tests.factories import (
    BoardGameFactory,
    PlayedBoardGameFactory,
    UserWith2GamesPlayedFactory,
    UserWithGamePlayedFactory,
)
from the_board_game_tracker.users.models import User

pytestmark = pytest.mark.django_db


def test_leaderboard_attributes():
    BoardGameFactory()  # unplayed board game
    game_player = UserWith2GamesPlayedFactory()
    assert models.BoardGame.objects.count() == 3

    users = User.objects.leaderboard()
    assert len(users) == 1
    assert users[0].username == game_player.username
    assert users[0].number_unplayed_games == 1
    assert users[0].completed_weight == 5


def test_leaderboard_ordering_games_played():
    # player_with 1 has played more recently but only the number of games
    # should count in this case
    player_with_1 = PlayedBoardGameFactory(
        date_played=datetime.date(2022, 1, 1)
    ).played_by
    player_with_2 = UserWith2GamesPlayedFactory(username="bob")

    users = User.objects.leaderboard()
    assert list(users) == [player_with_2, player_with_1]


@freeze_time("2022-01-01")
def test_leaderboard_ordering_tie_breaker_date():
    # alice has played 2 games and bob 1 game
    bob = UserWithGamePlayedFactory(username="bob")
    alice = UserWith2GamesPlayedFactory(username="alice")

    # bob plays a game more recently
    PlayedBoardGameFactory(played_by=bob, date_played=datetime.date(2022, 1, 12))

    # bob should be ahead while he has played more recently
    assert bob.games_played.count() == alice.games_played.count()
    assert list(User.objects.leaderboard()) == [bob, alice]


def test_leaderboard_ordering_tie_breaker_name():
    bob = UserWith2GamesPlayedFactory(username="bob")
    alice = UserWith2GamesPlayedFactory(username="alice")
    assert list(User.objects.leaderboard()) == [alice, bob]
