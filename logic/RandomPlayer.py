import numpy as np
from logic.Player import Player

class RandomPlayer(Player):
    def ask_decision(self, available_decisions):
        action = np.random.choice(available_decisions)
        if action == 'raise':
            return 'raise ' + str(np.random.randint(1, int(self.chips) / 10  + 1))
        return action

