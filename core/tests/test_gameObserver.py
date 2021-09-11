import unittest

from core.gameObserver import Clock, PlayOutcome, GameObserver


def checkTickFunction(clock, value, expectedMinVal, expectedSecVal, quarterFlagExp):
    quarterFlag = clock.tickDown(value)
    assert clock.minutes == expectedMinVal
    assert clock.seconds == expectedSecVal
    assert quarterFlag == quarterFlagExp


class TestGameObserver(unittest.TestCase):

    def test_down_change(self):
        gameObserver = GameObserver()

    def test_quarter_change(self):
        gameObserver = GameObserver()

    def test_end_game(self):
        gameObserver = GameObserver()

    def test_process_play_first_down(self):
        """Getting a first down"""
        gameObserver = GameObserver()
        gameObserver.down = 3
        gameObserver.yardsToGo = 6
        pr = PlayOutcome()
        pr.yardsGained = 11
        gameObserver.process_play(pr)
        assert gameObserver.down == 1
        assert gameObserver.yardsToGo == 10

    def test_process_play_any_down_not_enough_yards(self):
        """Gaining yards not First Down"""
        gameObserver = GameObserver()
        gameObserver.down = 2
        gameObserver.yardsToGo = 6
        pr = PlayOutcome()
        pr.yardsGained = 4
        gameObserver.process_play(pr)
        assert gameObserver.down == 3
        assert gameObserver.yardsToGo == 2

    def test_process_play_any_down_lost_yards(self):
        """Getting a first down"""
        gameObserver = GameObserver()
        gameObserver.down = 2
        gameObserver.yardsToGo = 6
        pr = PlayOutcome()
        pr.yardsGained = -4
        gameObserver.process_play(pr)
        assert gameObserver.down == 3
        assert gameObserver.yardsToGo == 10

    def test_process_play_turnover_on_downs(self):
        """Turnover on downs"""
        gameObserver = GameObserver()
        gameObserver.down = 4
        gameObserver.yardsToGo = 6
        pr = PlayOutcome()
        pr.yardsGained = 5
        gameObserver.process_play(pr)
        assert gameObserver.down == 1
        assert gameObserver.yardsToGo == 10
        self.assertFalse(gameObserver.possession)

    def test_process_clock(self):
        """Clock Processing"""
        gameObserver = GameObserver()
        gameObserver.process_clock(6)
        assert gameObserver.Clock.minutes == 14
        assert gameObserver.Clock.seconds == 54
        assert gameObserver.quarter == 1

    def test_process_clock_quarter_change(self):
        """Quarter Changing"""
        gameObserver = GameObserver()
        gameObserver.Clock.minutes = 0
        gameObserver.Clock.seconds = 5
        gameObserver.process_clock(6)
        assert gameObserver.Clock.minutes == 15
        assert gameObserver.Clock.seconds == 0
        assert gameObserver.quarter == 2

    def test_process_clock_end_game(self):
        """Quarter Changing"""
        gameObserver = GameObserver()
        gameObserver.quarter = 4
        gameObserver.Clock.minutes = 0
        gameObserver.Clock.seconds = 5
        gameObserver.process_clock(6)
        self.assertTrue(gameObserver.endGame)






class TestPlayOutcome(unittest.TestCase):

    def test_play_outcome_init(self):
        playOutcome = PlayOutcome()
        assert playOutcome.timeUsed == 0
        assert playOutcome.yardsGained == 0
        assert playOutcome.playCall == ''
        assert playOutcome.prevYards == 0


    def test_determine_yards_gained(self):
        temp = PlayOutcome()
        temp.determine_yards_gained()
        self.assertTrue(1 <= temp.yardsGained <= 10)

    def test_determine_play_called(self):
        temp = PlayOutcome()
        temp.determine_play_called()
        self.assertTrue(temp.playCall == 'pass' or temp.playCall == 'run')

    def test_determine_time_used(self):
        temp = PlayOutcome()
        temp.determine_time_used()
        self.assertTrue(1 <= temp.timeUsed <= 10)


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
