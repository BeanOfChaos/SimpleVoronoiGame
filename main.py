#!/usr/bin/python3
from voronoi_game import VoronoiGame
from uiplayer import UIPlayer
from config import W_WIDTH, W_HEIGHT
from botplayer import RandomBot

if __name__ == '__main__':
    # Hard definition of a simple square
    # TODO: randomly generate polygons for experiments
    polygon = [
               (W_WIDTH // 4, W_HEIGHT // 4),
               (3 * W_WIDTH // 4, W_HEIGHT // 4),
               (3 * W_WIDTH // 4, 3 * W_HEIGHT // 4),
               (W_WIDTH // 4, 3 * W_HEIGHT // 4)
               ]
    users = [(W_WIDTH//2, W_HEIGHT//2)]
    game = VoronoiGame(RandomBot(), UIPlayer(),
                       polygon=polygon, users=users)
    game.run()
