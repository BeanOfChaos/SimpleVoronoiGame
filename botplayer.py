from player import Player
from random import randint
import geometry as geo
import pygame as pg


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

    def optimal_p1(self, game, polygon, users):
        points = list(set(users).union(set(polygon)))
        internal_segs = []
        cell_vertices = set()
        mini = float('inf')
        for i, p1 in enumerate(points[:-1]):
            for j, p2 in enumerate(points[i+1:]):
                if p1 != p2 and geo.contains_full(p1, p2, polygon):
                    internal_segs.append((p1, p2))
        for i, seg1 in enumerate(internal_segs[:-1]):
            for j, seg2 in enumerate(internal_segs[i+1:]):
                inter = geo.segments_intersection(seg1[0], seg1[1],
                                                  seg2[0], seg2[1])
                if inter:
                    cell_vertices.add(inter)

        for candidate in cell_vertices:
            opponent_play = self.optimal_p2(candidate, polygon, users)
            opponent_score = game.compute_scores(candidate,
                                                 opponent_play)[1]
            if opponent_score < mini:
                opti = candidate
                mini = opponent_score
        return opti

    def optimal_p2(self, p1_play, polygon, users):
        regions = geo.nonvisibility_regions(p1_play, polygon)
        anchors = set()
        for user in users:
            found = False
            for anchor, region in regions:
                if geo.poly_contains(region, user):
                    anchors.add(anchor)
                    found = True
                    break
            if not found:
                anchors.add(user)
        anchors = list(anchors)
        line, side = geo.maximizing_half_plane(p1_play, anchors)
        a = line[0]
        pert1 = geo.normalize((side, side * a))
        way = side * a / abs(a)
        pert2 = geo.normalize((way, - way / a))
        perturb = ((pert1[0] + pert2[0]),
                   (pert1[1] + pert2[1]))

        return (p1_play[0] + perturb[0], p1_play[1] + perturb[1])

    def play(self, game):
        if game.p1_play is not None:
            return self.optimal_p2(game.p1_play, game.polygon, game.users)
        else:
            return self.optimal_p1(game, game.polygon, game.users)
