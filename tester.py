from Game import Game
from Player import Player
players = [Player(), Player()]
game = Game(10, 20, players, 1000)
game.start_game()

for i in range(5):
    for j in range(5):
        for k in range(5):
            if i != j and j != k and k != i:
                print(str(i) + " " + str(j) + " " + str(k))