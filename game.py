import time
from puzzle import Puzzle


class SlidingPuzzle:
    def __init__(self):
        self.size = 4
        self.puzzle = Puzzle(self.size)
        self.moves = 0
        self.started = time.monotonic()
        self.finished_at = None

    @property
    def finished(self):
        return self.finished_at is not None

    def elapsed(self):
        # The clock stops once the puzzle is solved.
        end = self.finished_at if self.finished else time.monotonic()
        return int(end - self.started)

    def display(self):
        print()
        for row in self.puzzle.board:
            print(" ".join(f"{x or ' ':>2}" for x in row))
        print("Moves:", self.moves, " Time:", self.elapsed(), "s")

    def slide(self, key):
        if self.finished:
            print("The puzzle is already solved; no more moves allowed.")
            return False
        if not self.puzzle.move(key):
            print("That move is not possible.")
            return False
        self.moves += 1
        if self.puzzle.solved():
            self.finished_at = time.monotonic()
        return True

    def run(self):
        print("Sliding Puzzle — W/A/S/D moves the tile into the blank. Q quits.")
        while True:
            self.display()
            if self.finished:
                print(f"Solved in {self.moves} moves and {self.elapsed()} s!")
                return
            key = input("> ").strip().lower()
            if key == "q":
                print("Quit without solving.")
                return
            if key not in "wasd":
                print("Use W/A/S/D.")
                continue
            self.slide(key)
