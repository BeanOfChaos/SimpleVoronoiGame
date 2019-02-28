import pygame as pg
import geometry
from colors import P1_COLOR, P2_COLOR, POLY_COLOR, USERS_COLOR, BG_COLOR
from config import W_HEIGHT, W_WIDTH


class VoronoiGame:

    def __init__(self, player1, player2, polygon=None, users=None):
        self.player1 = player1
        self.player2 = player2
        self.p1_play, self.p2_play = None, None
        self.polygon = polygon or []
        self.users = users or []
        assert(len(self.polygon) > 2 and len(self.users) > 0
               and all(geometry.poly_contains(self.polygon, user)
                       for user in self.users))
        self._step = 0
        self._action_handler = [self.player1_turn,
                                self.player2_turn,
                                self.compute_scores
                                ]

        pg.init()
        self.screen = pg.display.set_mode((W_WIDTH, W_HEIGHT))
        pg.display.set_caption('The Incredible Voronoi Game')

        # Fill board
        self.board = pg.Surface(self.screen.get_size()).convert()
        self.board.fill(BG_COLOR)

        # Blit everything to the screen
        self.screen.blit(self.board, (0, 0))
        self.running = False

    def show(self):
        self.screen.fill(BG_COLOR)
        pg.draw.polygon(self.screen, POLY_COLOR, self.polygon, 3)
        for user in self.users:
            pg.draw.circle(self.screen, USERS_COLOR, user, 3)
        if self.p1_play is not None:
            pg.draw.circle(self.screen, P1_COLOR, self.p1_play, 3)
        if self.p2_play is not None:
            pg.draw.circle(self.screen, P2_COLOR, self.p2_play, 3)
        pg.display.flip()

    def run(self):
        # TODO: polygon and users placement through GUI
        self.running = True
        while self.running:
            self.show()
            self.request_action()

    def is_valid_play(self, point):
        return geometry.poly_contains(self.polygon, point)

    def player_turn(self, player):
        point = player.play(self)
        while not self.is_valid_play(point):
            point = player.play(self)
        return point

    def player1_turn(self):
        self.p1_play = self.player_turn(self.player1)

    def player2_turn(self):
        self.p2_play = self.player_turn(self.player2)

    def request_action(self):
        self._action_handler[self._step]()
        self._step += 1
        self.running = self._step < len(self._action_handler)

    def compute_scores(self):
        score_p1 = 0
        score_p2 = 0
        for user in self.users:
            dist1 = geometry.distance_in_poly(self.p1_play, user, self.polygon)
            dist2 = geometry.distance_in_poly(self.p2_play, user, self.polygon)
            if dist1 < dist2:
                score_p1 += 1
            elif dist2 < dist1:
                score_p2 += 1
        print("Player 1's score: ", score_p1, "\nPlayer 2's score: ", score_p2)
        return score_p1, score_p2

    def reset(self):
        self.p1_play = None
        self.p2_play = None

    def end(self):
        pg.display.quit()
        pg.quit()
        exit(0)
