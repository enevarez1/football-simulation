import unittest

from core.gameObserver import Clock, PlayOutcome, GameObserver, Field


def checkTickFunction(clock, value, expectedMinVal, expectedSecVal, quarterFlagExp):
    quarterFlag = clock.tickDown(value)
    assert clock.minutes == expectedMinVal
    assert clock.seconds == expectedSecVal
    assert quarterFlag == quarterFlagExp


class TestGameObserver(unittest.TestCase):

    def test_quarter_change(self):
        game_observer = GameObserver()
        game_observer.Clock.minutes = 0
        game_observer.Clock.seconds = 4
        game_observer.quarter = 1
        game_observer.down = 3
        game_observer.yardsToGo = 6
        pr = PlayOutcome()
        pr.timeUsed = 5
        game_observer.process_play(pr)
        assert game_observer.quarter == 2

    def test_end_game(self):
        gameObserver = GameObserver()
        gameObserver.Clock.minutes = 0
        gameObserver.Clock.seconds = 4
        gameObserver.quarter = 4
        gameObserver.down = 3
        gameObserver.yardsToGo = 6
        pr = PlayOutcome()
        pr.timeUsed = 5
        gameObserver.process_play(pr)
        self.assertTrue(gameObserver.endGame)

    def test_process_play_first_down(self):
        """Getting a first down"""
        game_observer = GameObserver()
        game_observer.down = 3
        game_observer.yardsToGo = 6
        game_observer.Field.yard = 25
        game_observer.Field.side = "Own"
        pr = PlayOutcome()
        pr.yardsGained = 11
        game_observer.process_play(pr)

        assert game_observer.down == 1
        assert game_observer.yardsToGo == 10
        assert game_observer.Field.side == "Own"
        assert game_observer.Field.yard == 36

    def test_process_play_any_down_not_enough_yards(self):
        """Gaining yards not First Down"""
        game_observer = GameObserver()
        game_observer.down = 2
        game_observer.yardsToGo = 6
        pr = PlayOutcome()
        pr.yardsGained = 4
        game_observer.process_play(pr)
        assert game_observer.down == 3
        assert game_observer.yardsToGo == 2

    def test_process_play_any_down_lost_yards(self):
        """Getting a first down"""
        game_observer = GameObserver()
        game_observer.down = 2
        game_observer.yardsToGo = 6
        pr = PlayOutcome()
        pr.yardsGained = -4
        game_observer.process_play(pr)
        assert game_observer.down == 3
        assert game_observer.yardsToGo == 10

    def test_process_play_turnover_on_downs(self):
        """Turnover on downs"""
        game_observer = GameObserver()
        game_observer.down = 4
        game_observer.yardsToGo = 6
        pr = PlayOutcome()
        pr.yardsGained = 5
        game_observer.process_play(pr)
        assert game_observer.down == 1
        assert game_observer.yardsToGo == 10
        self.assertFalse(game_observer.possession)

    def test_process_clock(self):
        """Clock Processing"""
        game_observer = GameObserver()
        game_observer.process_clock(6)
        assert game_observer.Clock.minutes == 14
        assert game_observer.Clock.seconds == 54
        assert game_observer.quarter == 1

    def test_process_clock_quarter_change(self):
        """Quarter Changing"""
        game_observer = GameObserver()
        game_observer.Clock.minutes = 0
        game_observer.Clock.seconds = 5
        game_observer.process_clock(6)
        assert game_observer.Clock.minutes == 15
        assert game_observer.Clock.seconds == 0
        assert game_observer.quarter == 2

    def test_process_clock_end_game(self):
        """End Game"""
        game_observer = GameObserver()
        game_observer.quarter = 4
        game_observer.Clock.minutes = 0
        game_observer.Clock.seconds = 5
        game_observer.process_clock(6)
        self.assertTrue(game_observer.endGame)


class TestPlayOutcome(unittest.TestCase):

    def test_play_outcome_init(self):
        play_outcome = PlayOutcome()
        assert play_outcome.timeUsed == 0
        assert play_outcome.yardsGained == 0
        assert play_outcome.playCall == ''
        assert play_outcome.prevYards == 0

    def test_determine_yards_gained(self):
        temp = PlayOutcome()
        temp.determine_yards_gained()
        self.assertTrue(-10 <= temp.yardsGained <= 10)

    def test_determine_play_called(self):
        temp = PlayOutcome()
        temp.determine_play_called()
        self.assertTrue(temp.playCall == 'pass' or temp.playCall == 'run')

    def test_determine_time_used(self):
        temp = PlayOutcome()
        temp.determine_time_used()
        self.assertTrue(1 <= temp.timeUsed <= 10)


class TestField(unittest.TestCase):

    def test_own_yardage_gain(self):
        field = Field()
        field.side = 'Own'
        field.yard = 25
        field.process_yards(10)

        assert field.side == 'Own'
        assert field.yard == 35

    def test_opp_yardage_gain(self):
        field = Field()
        field.side = 'Opp'
        field.yard = 25
        field.process_yards(10)

        assert field.side == 'Opp'
        assert field.yard == 15

    def test_own_yardage_loss(self):
        field = Field()
        field.side = 'Own'
        field.yard = 25
        field.process_yards(-10)

        assert field.side == 'Own'
        assert field.yard == 15

    def test_opp_yardage_loss(self):
        field = Field()
        field.side = 'Opp'
        field.yard = 25
        field.process_yards(-10)

        assert field.side == 'Opp'
        assert field.yard == 35

    def test_own_yardage_gain_across_50(self):
        field = Field()
        field.side = 'Own'
        field.yard = 45
        field.process_yards(10)

        assert field.side == 'Opp'
        assert field.yard == 45

    def test_opp_yardage_loss_across_50(self):
        field = Field()
        field.side = 'Opp'
        field.yard = 45
        field.process_yards(-10)

        assert field.side == 'Own'
        assert field.yard == 45

    def test_yardage_land_on_50(self):
        field = Field()
        field.side = 'Own'
        field.yard = 40
        field.process_yards(10)

        assert field.side == 'None'
        assert field.yard == 50

    def test_touchdown_flag_opp(self):
        field = Field()
        field.side = 'Opp'
        field.yard = 30
        field.process_yards(30)

        self.assertTrue(field.touchdownFlag)

    def test_touchdown_flag_own(self):
        field = Field()
        field.side = 'Own'
        field.yard = 30
        field.process_yards(70)

        self.assertTrue(field.touchdownFlag)

    def test_safety_flag_opp(self):
        field = Field()
        field.side = 'Opp'
        field.yard = 30
        field.process_yards(-70)

        self.assertTrue(field.safetyFlag)

    def test_safety_flag_own(self):
        field = Field()
        field.side = 'Own'
        field.yard = 30
        field.process_yards(-30)

        self.assertTrue(field.safetyFlag)


class TestClock(unittest.TestCase):

    def test_clock_init(self):
        clock = Clock()
        assert clock.minutes == 15
        assert clock.seconds == 0

    def test_tick_handles_seconds_new_minute_at_zero(self):
        clock = Clock()
        checkTickFunction(clock, 12, 14, 48, False)

    def test_tick_handles_seconds(self):
        clock = Clock()
        clock.minutes = 0
        clock.seconds = 30
        checkTickFunction(clock, 29, 0, 1, False)

    def test_tick_handles_seconds_mid(self):
        clock = Clock()
        clock.minutes = 13
        clock.seconds = 15
        checkTickFunction(clock, 29, 12, 46, False)

    def test_tick_handles_new_quarter(self):
        clock = Clock()
        clock.minutes = 0
        clock.seconds = 15
        checkTickFunction(clock, 16, 15, 0, True)
