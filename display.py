#import shutil
#import time
#import sys
#from parsing import parse_config
#from maze_gen import MazeGenerator

#CONFIG = parse_config(sys.argv[1])

#class MazeRenderer:
#    COLORS = {
#        "white": "\033[97m",
#        "blue": "\033[94m",
#        "green": "\033[92m",
#        "yellow": "\033[93m",
#        "red": "\033[91m",
#        "reset": "\033[0m",
#    }
#    COLOR_NAMES = list(COLORS.keys())[:-1]
#    def __init__(self, maze: list[list[int]]) -> None:
#        self.maze = maze
#        self.maze_color = 0
#        self.logo_color = 0
#        self.sol_color = 2
#        self.animation_delay = 0.01
#        self.corner = "◆"
#        self.v_wall = "║"
#        self.h_wall = "═══"
#        self.block = "███"
#        self.space = "   "
#        self.entry = " ◉ "
#        self.exit = " ◎ "
#        self.path = " • "

#    def cycle_color(self, color) -> int:
#        return (color + 1) % len(self.COLOR_NAMES)

#    def _get_sol_char(self, char: str) -> str:
#        color = self.COLORS[self.COLOR_NAMES[self.sol_color]]
#        return f"{color}{char}{self.COLORS['reset']}"

#    def _get_wall_char(self, char: str) -> str:
#        color = self.COLORS[self.COLOR_NAMES[self.maze_color]]
#        return f"{color}{char}{self.COLORS['reset']}"

#    def _get_logo_char(self, char: str) -> str:
#        color = self.COLORS[self.COLOR_NAMES[self.logo_color]]
#        return f"{color}{char}{self.COLORS['reset']}"

#    def _path_to_coords(self,
#                        path: list[str],
#                        start: tuple[int, int]
#                        ) -> list[tuple[int, int]]:
#        DIRECTION_MAP = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
#        coords = [start]
#        row, col = start
#        for step in path:
#            dr, dc = DIRECTION_MAP[step]
#            row, col = row + dr, col + dc
#            coords.append((row, col))
#        return coords

#    def display_maze(
#            self,
#            grid: list[list[int]],
#            animate: bool,
#            display_solution: bool,
#            sol: list[str]
#            ) -> None:

#        height = len(grid)
#        width = len(grid[0])
#        NORTH = 1
#        WEST = 8
#        solution = self._path_to_coords(sol, CONFIG["ENTRY"])
#        for row in range(height):
#            top_line = ""
#            for col in range(width):
#                cell = grid[row][col]
#                top_line += self._get_wall_char(self.corner)
#                top_line += self._get_wall_char(
#                    self.h_wall if (cell & NORTH) else self.space
#                )
#            top_line += self._get_wall_char(self.corner)
#            if animate is True:
#                time.sleep(self.animation_delay)
#            print(top_line)

#            mid_line = ""
#            for col in range(width):
#                cell = grid[row][col]
#                mid_line += self._get_wall_char(
#                    self.v_wall if (cell & WEST) else " ")
#                if tuple([col, row]) == CONFIG["ENTRY"]:
#                    mid_line += self.entry
#                    continue
#                if tuple([col, row]) == CONFIG["EXIT"]:
#                    mid_line += self.exit
#                    continue
#                if display_solution is True:
#                    if tuple([row, col]) in solution:
#                        mid_line += self._get_sol_char(self.path)
#                        continue
#                mid_line += (
#                    self._get_logo_char(
#                        self.block) if cell == 15
#                        else self.space
#                )
#            mid_line += self._get_wall_char(self.v_wall)
#            if animate is True:
#                time.sleep(self.animation_delay)
#            print(mid_line)

#        bottom = ""
#        for col in range(width):
#            bottom += self._get_wall_char(self.corner)
#            bottom += self._get_wall_char(self.h_wall)
#        bottom += self._get_wall_char(self.corner)
#        if animate is True:
#            time.sleep(self.animation_delay)
#        print(bottom)

#    def check_fits(self, width: int, height: int) -> bool:
#        cols, rows = shutil.get_terminal_size()
#        needed_cols = width * 4 + 1
#        needed_rows = height * 2 + 1
#        return needed_cols <= cols and needed_rows <= rows


import shutil
import time
import sys
from parsing import parse_config
from maze_gen import MazeGenerator

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
        self.animation_delay = 0.01
        self.corner = "◆"
        self.v_wall = "║"
        self.h_wall = "═══"
        self.block = "███"
        self.space = "   "
        self.entry = " ◉ "
        self.exit = " ◎ "
        self.path = " • "

    def cycle_color(self, color) -> int:
        return (color + 1) % len(self.COLOR_NAMES)

    def _get_sol_char(self, char: str) -> str:
        color = self.COLORS[self.COLOR_NAMES[self.sol_color]]
        return f"{color}{char}{self.COLORS['reset']}"

    def _get_wall_char(self, char: str) -> str:
        color = self.COLORS[self.COLOR_NAMES[self.maze_color]]
        return f"{color}{char}{self.COLORS['reset']}"

    def _get_logo_char(self, char: str) -> str:
        color = self.COLORS[self.COLOR_NAMES[self.logo_color]]
        return f"{color}{char}{self.COLORS['reset']}"

    def _path_to_coords(self,
                        path: list[str],
                        start: tuple[int, int]
                        ) -> list[tuple[int, int]]:
        DIRECTION_MAP = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}
        coords = [start]
        row, col = start
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
                top_line += self._get_wall_char(self.corner)
                top_line += self._get_wall_char(
                    self.h_wall if (cell & NORTH) else self.space
                )
            top_line += self._get_wall_char(self.corner)
            if animate is True:
                time.sleep(self.animation_delay)
            print(top_line)

            mid_line = ""
            for col in range(width):
                cell = grid[row][col]
                mid_line += self._get_wall_char(
                    self.v_wall if (cell & WEST) else " ")
                if tuple([col, row]) == CONFIG["ENTRY"]:
                    mid_line += self.entry
                    continue
                if tuple([col, row]) == CONFIG["EXIT"]:
                    mid_line += self.exit
                    continue
                if display_solution is True:
                    if tuple([row, col]) in solution:
                        mid_line += self._get_sol_char(self.path)
                        continue
                mid_line += (
                    self._get_logo_char(
                        self.block) if cell == 15
                        else self.space
                )
            mid_line += self._get_wall_char(self.v_wall)
            if animate is True:
                time.sleep(self.animation_delay)
            print(mid_line)

        bottom = ""
        for col in range(width):
            bottom += self._get_wall_char(self.corner)
            bottom += self._get_wall_char(self.h_wall)
        bottom += self._get_wall_char(self.corner)
        if animate is True:
            time.sleep(self.animation_delay)
        print(bottom)

    def check_fits(self, width: int, height: int) -> bool:
        cols, rows = shutil.get_terminal_size()
        needed_cols = width * 4 + 1
        needed_rows = height * 2 + 1
        return needed_cols <= cols and needed_rows <= rows
