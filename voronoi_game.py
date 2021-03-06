import pygame as pg
import geometry
from colors import P1_COLOR, P2_COLOR, POLY_COLOR, USERS_COLOR, BG_COLOR
from config import W_HEIGHT, W_WIDTH


class VoronoiGame:
    """An implementation of the Voronoi Game in a simple polygon, where
       each player may place 1 facility. (Although this can be easily changed).
       A user is said to be served by a facility it it is the closest facility
       to that user. The player who serves the most users wins.
    """

    def __init__(self, player1, player2, polygon=None, users=None):
        self.player1 = player1
        self.player2 = player2
        self.p1_play, self.p2_play = None, None
        self.polygon = polygon or []
        self.users = users or []
        self.p1_score = None
        self.p2_score = None
        assert(len(self.polygon) > 2 and len(self.users) > 0
               and all(geometry.poly_contains(self.polygon, user)
                       for user in self.users))

        self.polygon = geometry.unknot_polygon(self.polygon)
        self._step = 0
        self._action_handler = [self.player1_turn,
                                self.player2_turn,
                                self.store_scores,
                                self.wait,
                                self.end
                                ]

        pg.init()
        self.width, self.height = W_WIDTH, W_HEIGHT
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption('The Incredible Voronoi Game')

        # Fill board
        self.board = pg.Surface(self.screen.get_size()).convert()
        self.board.fill(BG_COLOR)

        # Blit everything to the screen
        self.screen.blit(self.board, (0, 0))
        self.running = False

    def wait(self):
        self.show()
        input()

    def show(self):
        """Refreshes the display.
        """
        self.screen.fill(BG_COLOR)
        pg.draw.polygon(self.screen, POLY_COLOR, self.polygon, 3)
        for user in self.users:
            pg.draw.circle(self.screen, USERS_COLOR, user, 3)
        if self.p1_play is not None:
            pg.draw.circle(self.screen, P1_COLOR,
                           (int(self.p1_play[0]), int(self.p1_play[1])), 3)
        if self.p2_play is not None:
            pg.draw.circle(self.screen, P2_COLOR,
                           (int(self.p2_play[0]), int(self.p2_play[1])), 3)
        pg.display.flip()

    def run(self):
        """Launches the game, and executes every step.
        """
        # TODO: polygon and users placement through GUI
        self.running = True
        while self.running:
            self.show()
            self.request_action()

    def is_valid_play(self, point):
        """Checks if point is a valid play, i.e. if it lies inside of the
           polygon.
        """
        return geometry.poly_contains(self.polygon, point)

    def player_turn(self, player):
        """Requires a player to play, until it outputs a valid point.
        """
        point = player.play(self)
        while not self.is_valid_play(point):
            point = player.play(self)
        return point

    def player1_turn(self):
        print("P1, computing")
        self.p1_play = self.player_turn(self.player1)
        print("P1, played")

    def player2_turn(self):
        print("P2, computing")
        self.p2_play = self.player_turn(self.player2)
        print("P2, played")

    def request_action(self):
        """Executes a step of the game and prepares for the next.
           If it was the last, signals it.
        """
        self._action_handler[self._step]()
        self._step += 1
        self.running = self._step < len(self._action_handler)
        return self.running

    def compute_scores(self, p1_play, p2_play):
        """Computes the score for both players.
        """
        score_p1 = 0
        score_p2 = 0
        for user in self.users:
            dist1 = geometry.distance_in_poly(p1_play, user, self.polygon)
            dist2 = geometry.distance_in_poly(p2_play, user, self.polygon)
            if dist1 < dist2:
                score_p1 += 1
            elif dist2 < dist1:
                score_p2 += 1

        return (score_p1, score_p2)

    def store_scores(self):
        self.p1_score, self.p2_score = self.compute_scores(self.p1_play,
                                                           self.p2_play)
        print("Player 1's score: ", self.p1_score)
        print("Player 2's score: ", self.p2_score)
        if self.p1_score > self.p2_score:
            print("Player 1 wins!")
        elif self.p1_score < self.p2_score:
            print("Player 2 wins!")
        else:
            print("Tie!")

    # Unused for now
    def reset(self):
        """Erases players' plays and goes back to the first step.
        """
        self._step = 0
        self.p1_play = None
        self.p2_play = None

    def end(self):
        """Closes pygame and ends the program.
        """
        pg.display.quit()
        pg.quit()
