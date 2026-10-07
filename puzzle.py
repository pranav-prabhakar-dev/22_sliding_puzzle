import random

# Each key slides a tile in that direction into the blank, so the offset is
# where that tile sits relative to the blank (W = the tile below moves up).
DIRECTIONS = {"w": (1, 0), "s": (-1, 0), "a": (0, 1), "d": (0, -1)}
DIRECTION_NAMES = {"w": "up", "s": "down", "a": "left", "d": "right"}
OPPOSITE = {"w": "s", "s": "w", "a": "d", "d": "a"}


class Puzzle:
    def __init__(self, size=4):
        self.size = size
        self.board = self.make_board()

    def make_board(self):
        # Start solved and scramble with legal blank moves, so every board is reachable.
        tiles = list(range(1, self.size * self.size)) + [0]
        self.board = [tiles[r * self.size:(r + 1) * self.size] for r in range(self.size)]
        while self.solved():
            self.scramble(self.size * self.size * 20)
        return self.board

    def scramble(self, steps):
        last = None
        for _ in range(steps):
            options = [d for d in DIRECTIONS if d != OPPOSITE.get(last) and self.can_move(d)]
            last = random.choice(options)
            self.move(last)

    def can_move(self, direction):
        if direction not in DIRECTIONS:
            return False
        r, c = self.blank_pos()
        dr, dc = DIRECTIONS[direction]
        return 0 <= r + dr < self.size and 0 <= c + dc < self.size

    def blank_pos(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return r, c

    def move(self, direction):
        """Slide a tile into the blank. Return the moved tile's number, or None if no tile moved."""
        if not self.can_move(direction):
            return None
        r, c = self.blank_pos()
        dr, dc = DIRECTIONS[direction]
        nr, nc = r + dr, c + dc
        tile = self.board[nr][nc]
        self.board[r][c], self.board[nr][nc] = tile, 0
        return tile

    def solved(self):
        return sum(self.board, []) == list(range(1, self.size * self.size)) + [0]
