"""
Representation of a game state, pieces, grids, countdown...
"""

import md5
import sqlite3
import simplejson as json
from random import random
from datetime import datetime, timedelta

__all__ = ["GameState", "GridOverlaps", "BadSpot", "OutOfLife"]

db_path = None

types = ["circle", "cross"]


patterns = (
    (1, 1, 1, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 1, 1, 1, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 1, 1, 1),
    (1, 0, 0, 1, 0, 0, 1, 0, 0),
    (0, 1, 0, 0, 1, 0, 0, 1, 0),
    (0, 0, 1, 0, 0, 1, 0, 0, 1),
    (1, 0, 0, 0, 1, 0, 0, 0, 1),
    (0, 0, 1, 0, 1, 0, 1, 0, 0),
)


class GridOverlaps(Exception):
    pass
class BadSpot(Exception):
    pass
class OutOfLife(Exception):
    pass


class Piece(object):

    """A cross or circle element on the board."""

    def __init__(self, parent, x, y, type):
        self.gamestate = parent
        self.x = x
        self.y = y
        self.type = type
        self.color = "blank"

    def get_board_x(self):
        return self.gamestate.piece_dist * self.x
    board_x = property(get_board_x)

    def get_board_y(self):
        return self.gamestate.piece_dist * self.y
    board_y = property(get_board_y)

    def get_shape(self):
        return types[self.type]
    shape = property(get_shape)


class Grid(object):

    """A grouping of 9 pieces."""
    
    def __init__(self, parent, x, y, color):
        self.gamestate = parent
        self.x = x
        self.y = y
        self.color = color

    def get_board_x(self):
        return self.gamestate.piece_dist * self.x + self.gamestate.grid_offset
    board_x = property(get_board_x)

    def get_board_y(self):
        return self.gamestate.piece_dist * self.y + self.gamestate.grid_offset
    board_y = property(get_board_y)

    def extract_pattern(self, pattern, type=1):
        valid = []
        for x in range(3):
            for y in range(3):
                coords = (self.x + x, self.y + y)
                piece = self.gamestate.pieces[coords]
                if pattern[y * 3 + x] and piece.type == type:
                    valid.append(coords)
        
        if len(valid) == 3:
            return valid
        else:
            return []

    def extract(self, type=1):
        good = []
        for pattern in patterns:
            good += self.extract_pattern(pattern, type)
        return good


class GameState(object):

    """
    Maintain the game logic and state.
    """

    piece_size = 67
    piece_margin = 4
    piece_dist = piece_size + piece_margin * 2
    board_size = 32
    initial_countdown = 60
    grid_offset = 9
    
    def __init__(self, username):
        self.username = username
        self.gravatar = md5.md5("%s@reddit.com" % username.lower()).hexdigest()
        self.reset()

    def reset(self):
        self.recorded = False
        self.life = 100.0
        self.pieces = {}
        self.populate_pieces()
        self.grids = []
        self.finish = datetime.now() + timedelta(0, self.initial_countdown)
        self.troll_spots = []
        self.populate_trollspots()
        self.cool_lines = []
        self.populate_coollines()

    def populate_coollines(self):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM lines")
        count = cur.fetchone()[0]
        offset = int(random() * count)
        limit = min(60, count - offset)

        cur.execute("SELECT line FROM lines LIMIT %d OFFSET %d" % (limit, offset))
        self.cool_lines = [r[0] for r in cur.fetchall()]
        cur.close()
        conn.close()

    def cool_lines_as_json(self):
        return json.dumps(self.cool_lines);

    def populate_trollspots(self):
        """Generate x,y locations for good places to troll grids."""
        scored_grids = []
        for x in range(self.board_size - 3):
            for y in range(self.board_size - 3):
                grid = Grid(self, x, y, "pink")
                matches = grid.extract(type=0)
                if matches:
                    scored_grids.append((matches, grid))
        scored_grids.sort(key=lambda g: len(g[0]))
        self.troll_spots = scored_grids

    def populate_pieces(self):
        """Populate the crosses and circles.

        This information will be kept on the gamestate for the entire session
        or until the game is over.
        """
        for x in range(self.board_size):
            for y in range(self.board_size):
                p = Piece(self, x, y, int(random() + 0.5))
                self.pieces[(x, y)] = p

    def get_remaining(self):
        remaining = self.finish - datetime.now()
        return remaining.seconds
    remaining = property(get_remaining)

    def is_expired(self):
        return self.finish <= datetime.now()

    def overlaps(self, grid):
        """Check if a grid overlaps any other in the set."""
        for g in self.grids:
            if g is grid:
                continue
            if grid.x > g.x + 2 or grid.x < g.x - 2:
                continue
            if grid.y > g.y + 2 or grid.y < g.y - 2:
                continue
            return True

        return False

    def damage(self, amount):
        """Inflict damage to the player."""
        self.life -= amount
        if self.life <= 0:
            self.life = 0
            raise OutOfLife()

    def get_hiscores(self):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute("""
            SELECT name, score
            FROM scores
            ORDER BY score DESC
            LIMIT 5
            """)
        values = cur.fetchall()
        cur.close()
        conn.close()
        return values

    def record(self):
        if self.recorded:
            return
        stats = self.get_p1_stats()
        score = stats[1] * 1000 + stats[2] * -1000 + int(stats[0]) * 200
        self.recorded = True

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                name VARCHAR(128),
                score INTEGER
            )
            """)
        conn.commit()

        cur.execute("""
            INSERT INTO scores (name, score)
            VALUES (?, ?)
            """, (self.username, score))
        conn.commit()
        cur.close()
        conn.close()

    def add_grid(self, x, y, color):
        grid = Grid(self, x, y, color)
        self.grids.append(grid)

        if self.overlaps(grid):
            self.damage(10.0)
            grid.color = "red"
            raise GridOverlaps()

        matches = grid.extract()
        if not matches:
            self.damage(20)
            grid.color = "red"
            raise BadSpot()

        for coords in matches:
            self.pieces[coords].color = "green"

        return matches

    def next_troll_grid(self):
        while self.troll_spots:
            matches, grid = self.troll_spots.pop()
            if self.overlaps(grid):
                continue

            for coords in matches:
                self.pieces[coords].color = "pink"
            self.grids.append(grid)
            return matches, grid
        return None, None

    def get_p1_stats(self):
        good = len([p for p in self.pieces.values() if p.color == "green"])
        bad = len([g for g in self.grids if g.color == "red"])
        return (self.life, good, bad)

    def get_p2_stats(self):
        good = len([p for p in self.pieces.values() if p.color == "pink"])
        bad = 0
        return (100.0, good, bad)


def set_db_path(path):
    global db_path
    db_path = path
