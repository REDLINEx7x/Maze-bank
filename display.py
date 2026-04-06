import shutil
import time
import sys
from parsing import parse_config


CONFIG = parse_config(sys.argv[1])


class MazeRenderer:
    COLORS = {
        "white": "\033[97m",
        "blue": "\033[94m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "reset": "\033[0m",
    }
    COLOR_NAMES = list(COLORS.keys())[:-1]

    def __init__(self, maze: list[list[int]]) -> None:
        self.maze = maze
        self.maze_color = 0
        self.logo_color = 0
        self.sol_color = 2
        self.entry_color = 2
        self.exit_color = 4
        self.animation_delay = 0.01
        self.corner = "◆"
        self.v_wall = "║"
        self.h_wall = "═══"
        self.block = "███"
        self.space = "   "
        self.entry = " E "
        self.exit = " X "
        self.path = " ▪ "

    def cycle_color(self, color) -> int:
        return (color + 1) % len(self.COLOR_NAMES)

    def _get_char(self, char: str, color_index: int) -> str:
        color = self.COLORS[self.COLOR_NAMES[color_index]]
        return f"{color}{char}{self.COLORS['reset']}"

    def _path_to_coords(self,
                        path: list[str],
                        start: tuple[int, int]
                        ) -> list[tuple[int, int]]:
        DIRECTION_MAP = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
        col, row = start
        coords = []
        coords.append((row, col))
        for step in path:
            dr, dc = DIRECTION_MAP[step]
            row, col = row + dr, col + dc
            coords.append((row, col))
        return coords

    def display_maze(
            self,
            grid: list[list[int]],
            animate: bool,
            display_solution: bool,
            sol: list[str]
            ) -> None:

        height = len(grid)
        width = len(grid[0])
        NORTH = 1
        WEST = 8
        solution = self._path_to_coords(sol, CONFIG["ENTRY"])
        for row in range(height):
            top_line = ""
            for col in range(width):
                cell = grid[row][col]
                top_line += self._get_char(self.corner, self.maze_color)
                top_line += self._get_char(
                    self.h_wall if (cell & NORTH) else self.space,
                    self.maze_color
                )
            top_line += self._get_char(self.corner, self.maze_color)
            if animate is True:
                time.sleep(self.animation_delay)
            print(top_line)

            mid_line = ""
            for col in range(width):
                cell = grid[row][col]
                mid_line += self._get_char(
                    self.v_wall if (cell & WEST) else " ", self.maze_color)
                if tuple([col, row]) == CONFIG["ENTRY"]:
                    mid_line += self._get_char(self.entry, self.entry_color)
                    continue
                if tuple([col, row]) == CONFIG["EXIT"]:
                    mid_line += self._get_char(self.exit, self.exit_color)
                    continue
                if display_solution is True:
                    if tuple([row, col]) in solution:
                        mid_line += self._get_char(self.path, self.sol_color)
                        continue
                mid_line += (
                    self._get_char(
                        self.block, self.logo_color) if cell == 15 else self.space
                )
            mid_line += self._get_char(self.v_wall, self.maze_color)
            if animate is True:
                time.sleep(self.animation_delay)
            print(mid_line)

        bottom = ""
        for col in range(width):
            bottom += self._get_char(self.corner, self.maze_color)
            bottom += self._get_char(self.h_wall, self.maze_color)
        bottom += self._get_char(self.corner, self.maze_color)
        if animate is True:
            time.sleep(self.animation_delay)
        print(bottom)

    def check_fits(self, width: int, height: int) -> bool:
        cols, rows = shutil.get_terminal_size()
        needed_cols = width * 4 + 1
        needed_rows = height * 2 + 1
        return needed_cols <= cols and needed_rows <= rows
