import random

from gameObserver import GameObserver


class Match:

    def runGame(self):
        gameObserver = GameObserver()

        while gameObserver.clock is not 0.00:
            self.runPlay(GameObserver)


    def determinePlay(self):
        roll = random.randint(1,100)
        print(roll)
        if roll > 55:
            return 'pass'
        else:
            return 'run'

    def runPlay(self, gameObserver):
        playCall = self.determinePlay()

        if playCall == 'pass':
            # do a pass play
            # determine yards gained
            print('pass')
        elif playCall == 'run':
            # do a run play
            # determine yards gained
            print('run')