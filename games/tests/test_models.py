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
from the_board_game_tracker.users.models import LeaderBoardStates, User
from the_board_game_tracker.users.tests.factories import UserFactory

# NOTE: allows DB access by all tests in module
pytestmark = pytest.mark.django_db

TODAY = datetime.date.today()
COLD_DATE = TODAY - datetime.timedelta(days=29)
DEAD_DATE = TODAY - datetime.timedelta(days=91)
NORMAL_DATE = TODAY - datetime.timedelta(days=15)


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


@pytest.mark.parametrize(
    "exp_status, dates_played",
    [
        (LeaderBoardStates.HOT, [TODAY]),
        (LeaderBoardStates.HOT, [TODAY, NORMAL_DATE]),
        (LeaderBoardStates.HOT, [TODAY, NORMAL_DATE, COLD_DATE, DEAD_DATE]),
        (LeaderBoardStates.HOT, [TODAY, DEAD_DATE]),
        (LeaderBoardStates.HOT, [TODAY, COLD_DATE]),
        (LeaderBoardStates.NORMAL, [NORMAL_DATE]),
        (LeaderBoardStates.NORMAL, [NORMAL_DATE, COLD_DATE, DEAD_DATE]),
        (LeaderBoardStates.NORMAL, [NORMAL_DATE, DEAD_DATE]),
        (LeaderBoardStates.NORMAL, [NORMAL_DATE, COLD_DATE]),
        (LeaderBoardStates.COLD, [COLD_DATE]),
        (LeaderBoardStates.COLD, [COLD_DATE, DEAD_DATE]),
        (LeaderBoardStates.DEAD, [DEAD_DATE]),
    ],
)
def test_leaderboard_markers(exp_status, dates_played):
    """Only within the ranges of cold should it appear"""
    user = UserFactory()
    for date in dates_played:
        PlayedBoardGameFactory(played_by=user, date_played=date)

    assert User.objects.leaderboard()[0].status == exp_status


@pytest.mark.parametrize(
    "last_new, replayed_date, exp_status",
    [
        (TODAY, TODAY, LeaderBoardStates.HOT),
        # will restore normal but not hot
        (COLD_DATE, TODAY, LeaderBoardStates.NORMAL),
        (DEAD_DATE, TODAY, LeaderBoardStates.NORMAL),
        # will downgrade state
        (DEAD_DATE, COLD_DATE, LeaderBoardStates.COLD),
    ],
)
def test_leaderboard_markers_with_new_replayed(last_new, replayed_date, exp_status):
    """Only within the ranges of cold should it appear"""
    user = UserFactory(replayed_game_date=replayed_date)
    PlayedBoardGameFactory(played_by=user, date_played=last_new)

    assert User.objects.leaderboard()[0].status == exp_status
