import numpy as np

from Player import Player
import numpy

class RandomPlayer(Player):
    def ask_decision(self):
        decisions = ['raise', 'call', 'fold', 'check']
        action = np.random.choice(decisions)
        if action == 'raise':
            return 'raise ' + str(numpy.random.randint(1, int(self.chips) / 10  + 1))
        return action

