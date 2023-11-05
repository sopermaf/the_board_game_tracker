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
    UserFactory()  # user without games played
    BoardGameFactory()  # unplayed board game
    game_player = UserWith2GamesPlayedFactory()
    PlayedBoardGameFactory(played_by__is_visible=False)
    assert models.BoardGame.objects.count() == 4

    best_player = User.objects.leaderboard().first()
    assert best_player
    assert best_player.username == game_player.username
    assert best_player.number_unplayed_games == 2
    assert best_player.completed_weight == 5
    assert best_player.status in LeaderBoardStates

    new_player = User.objects.leaderboard().last()
    assert new_player.status == LeaderBoardStates.DEAD


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


def test_played_games_updates():
    # ensure done per day and per game
    # 2 games, over 3 days should be 6 entries total
    catan = BoardGameFactory(name="catan")
    cards = BoardGameFactory(name="cards")

    jack = UserFactory(username="jack")
    joe = UserFactory(username="joe")

    PlayedBoardGameFactory(played_by=jack, board_game=cards, date_played=COLD_DATE)

    # Joe and John have a games session and play 2 games
    for user in [joe, jack]:
        PlayedBoardGameFactory(played_by=user, board_game=catan, date_played=TODAY)
    PlayedBoardGameFactory(played_by=joe, board_game=cards, date_played=TODAY)

    updates_qs = models.PlayedBoardGame.objects.newly_played_updates()
    assert list(updates_qs) == [
        {
            "date_played": TODAY,
            "games": catan.name,
            "played_by__username": jack.username,
        },
        {
            "date_played": TODAY,
            "games": ", ".join(g.name for g in (cards, catan)),
            "played_by__username": joe.username,
        },
        {
            "date_played": COLD_DATE,
            "games": cards.name,
            "played_by__username": jack.username,
        },
    ]


def test_games_played_chart_data():
    UserFactory(username="joe")
    PlayedBoardGameFactory.create_batch(
        size=3, played_by__username="jack", date_played=DEAD_DATE
    )
    PlayedBoardGameFactory.create_batch(
        size=2, played_by__username="jill", date_played=DEAD_DATE
    )
    PlayedBoardGameFactory(played_by__username="jack", date_played=COLD_DATE)

    qs = models.PlayedBoardGame.objects.game_played_over_time_annotation()
    assert list(qs) == [
        {
            "date_played": DEAD_DATE,
            "jack": 3,
            "jill": 2,
        },
        {
            "date_played": COLD_DATE,
            "jack": 4,
            "jill": 2,
        },
    ]
