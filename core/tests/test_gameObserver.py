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
        gameObserver.run_play()
        assert gameObserver.down == 2
        assert gameObserver.yards ==

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
