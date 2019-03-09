#!/usr/bin/python3
import geometry as geo
from voronoi_game import VoronoiGame
from uiplayer import UIPlayer
from config import W_WIDTH, W_HEIGHT
from botplayer import RandomBot

from random import randint


def random_polygon(n_vertices):
    poly = [(randint(0, W_WIDTH), randint(0, W_HEIGHT))
            for i in range(n_vertices)]
    poly = geo.unknot_polygon(poly)
    return poly


def random_users(n_users, poly):
    users = set()
    while n_users:
        point = (randint(0, W_WIDTH), randint(0, W_HEIGHT))
        if geo.poly_contains(poly, point) and point not in users:
            users.add(point)
            n_users -= 1
    return users


if __name__ == '__main__':
    # Hard definition of a simple square
    # TODO: randomly generate polygons for experiments
    polygon = random_polygon(randint(4, 20))
    users = random_users(10, polygon)
    game = VoronoiGame(UIPlayer(), UIPlayer(),
                       polygon=polygon, users=users)
    game.run()
