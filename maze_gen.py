from typing import Any, Callable, Optional
import random
from collections import deque
from parsing import parse_config
NORTH = 1
EAST  = 2
SOUTH = 4
WEST  = 8

DIRECTIONS = {
    NORTH: (-1,  0, SOUTH),
    EAST:  ( 0, +1, WEST),
    SOUTH: (+1,  0, NORTH),
    WEST:  ( 0, -1, EAST),
}

class MazeGenerator:

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        #seed: Optional[int] = None,
        perfect: bool = True,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry   # (col, row) = (x, y)
        self.exit = exit
        self.perfect = perfect
        self.grid: list[list[int]] = []
        self.solution: list[str] = []

    def generate(self):
            #import random
            #random.seed(self.seed)      # we need to add seed in config_file

            self._init_grid()           # 1. all walls closed
            #self._create_42_pattern()            # 5. for "42" pattern
            self._carve()               # 2. carve passages
            #self._open_borders()        # 3. open entry/exit
            #if not self.perfect:
            #    self._add_loops()       # 4. optional: extra paths
            #self.solution = self._solve() # 6. find the path

    def _init_grid(self):
            # Fill every cell with 15 = all walls closed
            self.grid = [
            [15 for _ in range (self.width)]
            for _ in range(self.height)
        ]

    def _creatr_42_pattern(self, visited: list[list[bool]]):

        pattern = [
            "#   ###",
            "#     #",
            "### ###",
            "  # #  ",
            "  # ###"
        ]
        patt_height = len(pattern)
        patt_width = len(pattern[0])

        if(self.height < patt_height + 2 and self.width > patt_width + 2):
             return

        start_row = (self.height - patt_height) // 2
        start_col = (self.width - patt_width) // 2

        for po_r, line in enumerate(pattern):
             for po_c, char in enumerate(line):
                  if char == "#":
                    r, c = start_row + po_r, start_col + po_c
                    self.grid[r][c] = 15
                    visited[r][c] = True
    def _carve(self):
        # Track which cells we've visited
        visited = [
        [False] * self.width
        for _ in range(self.height)
        ]
        start_row = self.entry[1]
        start_col = self.entry[0]
        self._creatr_42_pattern(visited)
        self._starting_carve(start_row, start_col, visited)

    def _starting_carve(self, row: int, col: int, visited: list[list[bool]]) -> None:

        visited[row][col] = True
        dir = list(DIRECTIONS.items())
        random.shuffle(dir)

        for direction, (dr, dc, opposite) in dir:
            new_row = row + dr
            new_col = col + dc

            # Skip if out of bounds
            if not (0 <= new_row < self.height):
                continue
            if not (0 <= new_col < self.width):
                continue

            # Skip if already visited
            if visited[new_row][new_col]:
                continue

            # Remove wall on BOTH sides
            self.grid[row][col]           &= ~direction
            self.grid[new_row][new_col]   &= ~opposite

            # Recurse into the neighbor
            self._starting_carve(new_row, new_col, visited)


config_data = parse_config("config.txt")

maze = MazeGenerator(
    width=config_data['WIDTH'],
    height=config_data['HEIGHT'], # Reproducibility daroriya
    entry=config_data['ENTRY'],
    exit=config_data['EXIT'],
    perfect=config_data['PERFECT'],
)

# maze.generate()

# print(maze.grid)
