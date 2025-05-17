
import numpy as np


class RPStrainer():
    def __init__(self):
        self.number_of_actions = 3
        self.available_moves = np.arange(3)
        # available_actions are index: [0] - rock, [1] - paper, [2] - scissors
        # [0][1] is the reward you get if you play rock and opponent plays paper
        self.available_rewards = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])

        self.strategy_sum = np.zeros(self.number_of_actions)
        self.regret_sum = np.zeros(self.number_of_actions)

    def get_strategy(self):
        # get_strategy will return the probabilty of playing r, p, s in current move
        actual_regret = np.clip(self.regret_sum, 0, a_max=None)
        if np.sum(actual_regret) == 0:
            return np.repeat(1 / self.number_of_actions, self.number_of_actions)
        else:
            return actual_regret / sum(actual_regret)

    def train(self, iterations):
        for i in range(iterations):
            player_strategy = self.get_strategy()

            player_move = np.random.choice(self.available_moves, p = player_strategy)

            opponent_move = 2

            player_reward = self.available_rewards[player_move, opponent_move]

            player_regrets = np.zeros(self.number_of_actions)

            for action  in self.available_moves:
                player_regrets[action] = self.available_rewards[action, opponent_move] - player_reward
            self.regret_sum += player_regrets

rps = RPStrainer()
rps.train(10)
print(rps.get_strategy())
