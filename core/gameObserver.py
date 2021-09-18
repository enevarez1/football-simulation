import random
from enum import Enum


class GameObserver:
    def __init__(self):
        self.Clock = Clock()
        self.Field = Field()
        self.quarter = 1
        self.possession = True  # true(home)/false(away)
        self.homeScore = 0
        self.awayScore = 0
        self.down = 1
        self.yardsToGo = 10
        self.kickoffFlag = True
        self.endGame = False

    def run_game(self):
        while not self.endGame:
            self.run_play()

    def run_play(self):
        play_outcome = PlayOutcome()
        play_outcome.run_all_functions()
        self.process_play(play_outcome)

    def process_play(self, PlayOutcome):
        """Check all scenarios that can happen after a play"""

        if PlayOutcome.yardsGained > self.yardsToGo:
            """Getting a first down"""
            self.down = 1
            self.yardsToGo = 10
        elif self.down == 4 and PlayOutcome.yardsGained < self.yardsToGo:
            """Turnover on downs"""
            self.possession = not self.possession
            self.down = 1
            self.yardsToGo = 10
        elif PlayOutcome.yardsGained < self.yardsToGo:
            """Changing Yards"""
            self.down += 1
            self.yardsToGo = self.yardsToGo - PlayOutcome.yardsGained

        self.Field.process_yards(PlayOutcome.yardsGained)
        self.process_clock(PlayOutcome.timeUsed)

    def process_clock(self, time_used):
        quarter_flag_check = self.Clock.tickDown(time_used)
        if quarter_flag_check:
            self.quarter += 1
        if self.quarter > 4:
            self.endGame = True


class PlayOutcome:
    def __init__(self):
        self.timeUsed = 0
        self.yardsGained = 0
        self.playCall = ''
        self.prevYards = 0

    def determine_yards_gained(self):
        self.yardsGained = random.randint(-10, 10)

    def determine_play_called(self):
        temp = random.randint(0, 1)
        if temp == 0:
            self.playCall = 'pass'
        else:
            self.playCall = 'run'

    def determine_time_used(self):
        self.timeUsed = random.randint(1, 10)

    def run_all_functions(self):
        self.determine_yards_gained()
        self.determine_play_called()
        self.determine_time_used()


class Result(Enum):
    COMPLETION = 'COMPLETION'
    INCOMPLETION = 'INCOMPLETION'
    THROWN_AWAY = 'THROWN_AWAY'
    FUMBLE = 'FUMBLE'
    FUMBLE_SACK = 'FUMBLE_SACK'
    FUMBLE_LOSS = 'FUMBLE_LOSS'
    INTERCEPTION = 'INTERCEPTION'
    SACK = 'SACK'
    PASS_DEFLECTION = 'PASS_DEFLECTION'
    RUSH_FOR_LOSS = 'RUSH_FOR_LOSS'
    DROPPED_PASS = 'DROPPED_PASS'


class Penalty(Enum):
    FALSE_START = 'FALSE_START'
    DELAY_OF_GAME = 'DELAY_OF_GAME'
    ILLEGAL_FORMATION = 'ILLEGAL_FORMATION'
    ILLEGAL_SHIFT = 'ILLEGAL_SHIFT'
    OFFENSIVE_PASS_INTERFERENCE = 'OFFENSIVE_PASS_INTERFERENCE'
    DEFENSIVE_PASS_INTERFERENCE = 'DEFENSIVE_PASS_INTERFERENCE'
    CLIPPING = 'CLIPPING'
    CHOP_BLOCK = 'CHOP_BLOCK'
    ENCROACHMENT = 'ENCROACHMENT'
    HOLDING = 'HOLDING'
    HORSE_COLLAR_TACKLE = 'HORSE_COLLAR_TACKLE'
    ILLEGAL_BLOCK_IN_BLACK = 'ILLEGAL_BLOCK_IN_BLACK'
    ILLEGAL_HANDS = 'ILLEGAL_HANDS'


class Field:

    def __init__(self):
        self.side = "None"  # Could be None(50), Own, and Opp
        self.yard = 50
        self.safetyFlag = False
        self.touchdownFlag = False

    def process_yards(self, result_yards):

        if self.side == "Own":
            self.yard += result_yards

        if self.side == "Opp":
            self.yard -= result_yards

        if self.yard > 50:
            if self.side == "Opp":
                self.side = "Own"
            elif self.side == "Own":
                self.side = "Opp"
            self.yard = 50 - (self.yard - 50)
            print(self.yard)
        elif self.yard == 50:
            self.side = "None"
        if self.yard <= 0:
            if result_yards > 0:
                self.touchdownFlag = True
            else:
                self.safetyFlag = True


class Clock:

    def __init__(self):
        self.minutes = 15
        self.seconds = 0

    def newQuarter(self):
        self.minutes = 15
        self.seconds = 0
        return True

    def tickDown(self, secondsToRemove):
        self.seconds -= secondsToRemove

        if self.seconds < 0:
            self.seconds = 60 - (0 - self.seconds)
            self.minutes -= 1

        if self.minutes < 0:
            return self.newQuarter()
        else:
            return False
