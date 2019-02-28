import pygame as pg

from player import Player


class UIPlayer(Player):

    def __init__(self):
        pass

    def play(self, game):
        while True:
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONUP:
                    return event.pos
