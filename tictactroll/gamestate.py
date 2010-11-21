"""
Representation of a game state, pieces, grids, countdown...
"""

from random import random
from datetime import datetime, timedelta
import md5


types = ["circle", "cross"]


class GameState(object):

    piece_size = 67
    piece_margin = 4
    piece_dist = piece_size + piece_margin * 2
    board_size = 32
    initial_countdown = 60
    
    def __init__(self, username):
        self.username = username
        self.gravatar = md5.md5("%s@reddit.com" % username.lower()).hexdigest()

        self.pieces = []
        self.populate_pieces()

        self.grids = []

        self.finish = datetime.now() + timedelta(0, self.initial_countdown)

    def populate_pieces(self):
        """Populate the crosses and circles.

        This information will be kept on the gamestate for the entire session
        or until the game is over.
        """
        for x in range(self.board_size):
            for y in range(self.board_size):
                self.pieces.append((x * self.piece_dist, y * self.piece_dist,
                        types[int(random() + 0.5)]))

    def get_remaining(self):
        remaining = self.finish - datetime.now()
        return remaining.seconds
    remaining = property(get_remaining)

    def add_grid(self, x, y):
        self.grids.append((x, y, 

