import time
from puzzle import DIRECTION_NAMES, DIRECTIONS, Puzzle

SIZES = (3, 4, 5)
DEFAULT_SIZE = 4


def read(prompt):
    # Treat Ctrl+C / end of input as a request to quit instead of crashing.
    try:
        return input(prompt).strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return "q"


class SlidingPuzzle:
    def __init__(self):
        # Session values: kept for the whole run, never touched by new_board().
        self.session_started = time.monotonic()
        self.boards_played = 0
        self.boards_solved = 0
        self.total_moves = 0
        self.size = DEFAULT_SIZE
        self.puzzle = None

    def new_board(self, size):
        # Per-board values only: a fresh board starts its own move count and clock.
        self.size = size
        self.puzzle = Puzzle(size)
        self.moves = 0
        self.started = time.monotonic()
        self.finished_at = None
        self.boards_played += 1

    @property
    def finished(self):
        return self.finished_at is not None

    def elapsed(self):
        # The clock stops once the puzzle is solved.
        end = self.finished_at if self.finished else time.monotonic()
        return int(end - self.started)

    def session_elapsed(self):
        return int(time.monotonic() - self.session_started)

    def ask_size(self):
        """Return a board size, or None if the player wants to quit."""
        while True:
            choice = read(f"Board size 3, 4 or 5 [Enter = {self.size}, Q quits]: ")
            if choice == "q":
                return None
            if choice == "":
                return self.size
            if choice.isdigit() and int(choice) in SIZES:
                return int(choice)
            print("Please enter 3, 4 or 5.")

    def display(self):
        print()
        for row in self.puzzle.board:
            print(" ".join(f"{x or ' ':>2}" for x in row))
        print(f"Size: {self.size}x{self.size}  Moves: {self.moves}  Time: {self.elapsed()} s")
        if self.finished:
            print(f"Solved in {self.moves} moves and {self.elapsed()} s! N for a new board, Q quits.")

    def session_summary(self):
        print(
            f"Session: {self.boards_played} board(s), {self.boards_solved} solved, "
            f"{self.total_moves} total moves, {self.session_elapsed()} s."
        )

    def slide(self, key):
        if self.finished:
            print("The puzzle is already solved; no more moves allowed.")
            return False
        tile = self.puzzle.move(key)
        if tile is None:
            print(f"No tile can move {DIRECTION_NAMES[key]} into the blank.")
            return False
        print(f"Moved tile {tile} {DIRECTION_NAMES[key]}.")
        self.moves += 1
        self.total_moves += 1
        if self.puzzle.solved():
            self.finished_at = time.monotonic()
            self.boards_solved += 1
        return True

    def quit(self):
        if self.puzzle is not None and not self.finished:
            print("Quit without solving.")
        self.session_summary()

    def run(self):
        print("Sliding Puzzle - W/A/S/D slides a tile up/left/down/right into the blank.")
        print("N starts a new board, Q quits.")
        size = self.ask_size()
        if size is None:
            return self.quit()
        self.new_board(size)
        while True:
            self.display()
            key = read("> ")
            if key == "q":
                return self.quit()
            if key == "n":
                size = self.ask_size()
                if size is None:
                    return self.quit()
                self.new_board(size)
                continue
            if key not in DIRECTIONS:
                print(f"Unknown command {key!r}. Use W/A/S/D, N or Q.")
                continue
            self.slide(key)
