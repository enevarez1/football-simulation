import random
from enum import Enum


class GameObserver:
    def __init__(self):
        self.Clock = Clock()
        self.quarter = 1
        self.possession = 'home' #'home'/'away', || true(home)/false(away)
        self.down = 1
        self.kickoffFlag = True


        def runPlay():



class PlayOutcome:
    def __init__(self):
        self.timeUsed = 0
        self.yardsGained = 0
        self.playCall = ''
        self.prevYards = 0

    def determine_yards_gained(self):
        self.yardsGained = random.randint(1, 10)

    def determine_play_called(self):
        temp = random.randint(0, 1)
        if temp == 0:
            self.playCall = 'pass'
        else:
            self.playCall = 'run'

    def determine_time_used(self):
        self.timeUsed = random.randint(1, 10)


class Result(Enum):
    COMPLETION = 'COMPLETION'
    INCOMPLETION = 'INCOMPLETION'
    THROWN_AWAY = 'THROWN_AWAY'
    FUMBLE = 'FUMBLE'
    FUMBLE_SACK = 'FUMBLE_SACK'
    FUMBLE_LOSS = 'FUMBLE_LOSS'
    INTERCEPTION =  'INTERCEPTION'
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

        if(self.seconds < 0):
            temp = 0 - self.seconds
            self.seconds = 60 - temp
            self.minutes -= 1

        if(self.minutes < 0):
             return self.newQuarter()
        else:
            return False






