import pygame as pg
from player import Player


class UIPlayer(Player):
    """A player that interacts with the game through pygame GUI.
    """
    def __init__(self):
        pass

    def play(self, game):
        """Retrieves the player's action, and returns it.
        """
        while True:
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP:
                    return event.pos
                elif event.type == pg.QUIT:
                    exit(0)
