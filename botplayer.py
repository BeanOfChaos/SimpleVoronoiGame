from player import Player
from random import randint


class RandomBot(Player):
    """A simple bot that plays randomly.
       Note that whether the play is valid or not is left to decide to the game
       itself.
    """

    def __init__(self):
        pass

    def play(self, game):
        x, y = randint(0, game.width), randint(0, game.height)
        return x, y


class OptimalBot(Player):

    def __init__(self):
        pass

    def play(self, game):
        if game.p1_play:
            # TODO: insert algorithm for first player
            pass
        else:
            # TODO: insert algorithm for second player
            pass
