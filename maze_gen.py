from typing import Any, Callable, Optional
import random
from collections import deque
from parsing import parse_config
from maze_solve import solve

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
        seed: Optional[int] = None,
        perfect: bool = True,
    ) -> None:

        self.width = width
        self.height = height
        self.entry = entry   # (col, row) = (x, y)
        self.exit = exit
        self.perfect = perfect
        self.seed = seed
        self.grid: list[list[int]] = []

    def generate(self):

        # random.seed(self.seed)      # we need to add seed in config_file
        self._init_grid()           # 1. all walls closed         # 5. for "42" pattern
        self._carve()               # 2. carve passages
        if not self.perfect:
            self._add_extra_paths()       # 4. optional: extra paths
    def _init_grid(self):
            self.grid = [
            [15 for _ in range (self.width)]
            for _ in range(self.height)
        ]

    def _create_42_pattern(self, visited: list[list[bool]]):

        pattern = [
            "#   ###",
            "#     #",
            "### ###",
            "  # #  ",
            "  # ###"
        ]
        patt_height = len(pattern)
        patt_width = len(pattern[0])

        if(self.height < patt_height + 2 or self.width < patt_width + 2):
             return

        start_row = (self.height - patt_height) // 2
        start_col = (self.width - patt_width) // 2
        entry_cell = (self.entry[1], self.entry[0])
        exit_cell  = (self.exit[1],  self.exit[0])

        for po_r, line in enumerate(pattern):
             for po_c, char in enumerate(line):
                  if char == "#":
                    r = start_row + po_r
                    c = start_col + po_c
                    if (r, c) == entry_cell or (r, c) == exit_cell:
                        continue
                    self.grid[r][c] = 0xF
                    visited[r][c] = True
    def _carve(self):
        # Track which cells we've visited
        visited = [
        [False] * self.width
        for _ in range(self.height)
        ]
        start_row = self.entry[1]
        start_col = self.entry[0]
        self._create_42_pattern(visited)
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
            self._starting_carve(new_row, new_col, visited)

    def _add_extra_paths(self):

        total_cells = self.height * self.width
        nedded_walls = total_cells // 10
        removed = 0
        tries  = 0
        while removed < nedded_walls and tries < 1000:
            tries += 1
            row = random.randint(0, self.height - 2)
            col = random.randint(0, self.width - 2)
            to_east = random.choice([True, False])
            if to_east:
                if self.grid[row][col] == 15:
                    continue
                if self.grid[row][col + 1] == 15:
                    continue
                if self.grid[row][col] & EAST:
                    self.grid[row][col] &= ~EAST
                    self.grid[row][col + 1] &= ~WEST
                    if self._has_3x3_open(row, col):
                        self.grid[row][col] |= EAST
                        self.grid[row][col + 1] |= WEST
                        continue
                    removed += 1
                else:
                    continue

            else:
                if self.grid[row][col] == 15:
                    continue
                if self.grid[row + 1][col] == 15:
                    continue
                if self.grid[row][col] & SOUTH:
                    self.grid[row][col] &= ~SOUTH
                    self.grid[row + 1][col] &= ~NORTH
                    if self._has_3x3_open(row, col):
                        self.grid[row][col] |= SOUTH
                        self.grid[row + 1][col] |= NORTH
                        continue

                    removed += 1
                else:
                    continue


    def _has_3x3_open(self, row: int, col: int) -> bool:

        for r in range(row - 2, row + 2):
            for c in range(col - 2, col + 2):
                # bounds check — is this 3x3 block inside the grid?
                if r < 0 or c < 0:
                    continue
                if r + 2 >= self.height or c + 2 >= self.width:
                    continue
                # check all internal walls of this 3x3 block
                all_open = True
                for dr in range(3):
                    for dc in range(3):
                        cr = r + dr
                        cc = c + dc
                        # check East wall (not last column of block)
                        if dc < 2:
                            if self.grid[cr][cc] & EAST:
                                all_open = False
                                break
                        # check South wall (not last row of block)
                        if dr < 2:
                            if self.grid[cr][cc] & SOUTH:
                                all_open = False
                                break
                    if not all_open:
                        break
                if all_open:
                    return True
        return False

# def display_maze_with_solution(grid: list[list[int]], entry: tuple[int, int], path: list[str]) -> None:
#     height = len(grid)
#     width = len(grid[0])

#     solution_cells = set()
#     curr_r, curr_c = entry[1], entry[0]
#     solution_cells.add((curr_r, curr_c))

#     for move in path:
#         if move == 'N': curr_r -= 1
#         elif move == 'S': curr_r += 1
#         elif move == 'E': curr_c += 1
#         elif move == 'W': curr_c -= 1
#         solution_cells.add((curr_r, curr_c))

#     # 2. R-Resm
#     print("+" + "---+" * width)

#     for r, row in enumerate(grid):
#         line = "|"
#         for c, cell in enumerate(row):
#             char = " . " if (r, c) in solution_cells else "   "

#             if cell & 2:
#                 line += char + "|"
#             else:
#                 line += char + " "
#         print(line)

#         bottom = "+"
#         for c, cell in enumerate(row):
#             if cell & 4:
#                 bottom += "---+"
#             else:
#                 bottom += "   +"
#         print(bottom)
# try:
#     config_data = parse_config("config.txt")

#     maze = MazeGenerator(
#         width=config_data['WIDTH'],
#         height=config_data['HEIGHT'], # Reproducibility daroriya
#         entry=config_data['ENTRY'],
#         exit=config_data['EXIT'],
#         perfect=config_data['PERFECT'],
#         seed=config_data['SEED'],
#     )

#     maze.generate()
#     path = solve(maze.grid, maze.entry, maze.exit, maze.width, maze.height)
#     display_maze_with_solution(maze.grid, maze.entry, path)
#     print(path)
# except Exception as e:
#     print(e)
