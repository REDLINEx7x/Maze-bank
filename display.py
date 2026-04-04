import shutil
import time
import os
from parsing import CONFIG
from maze_gen import MazeGenerator


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

    def _get_wall_char(self, char: str) -> str:
        color = self.COLORS[self.COLOR_NAMES[self.maze_color]]
        return f"{color}{char}{self.COLORS['reset']}"

    def _get_logo_char(self, char: str) -> str:
        color = self.COLORS[self.COLOR_NAMES[self.logo_color]]
        return f"{color}{char}{self.COLORS['reset']}"

    def display_maze(self, grid: list[list[int]], animate: bool) -> None:
        height = len(grid)
        width = len(grid[0])
        NORTH = 1
        WEST = 8

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
                mid_line += (
                    self._get_logo_char(
                        self.block) if cell == 15 else self.space
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


def validate_entry_exit(
        entry: tuple[int, int],
        exit: tuple[int, int],
        maze: list[list[int]]) -> None:

    ex, ey = entry
    xx, xy = exit
    height = len(maze)
    width = len(maze[0])

    if not (0 <= ex < width and 0 <= ey < height):
        raise ValueError(f"Entry {entry} is outside the maze bounds.")

    if not (0 <= xx < width and 0 <= xy < height):
        raise ValueError(f"Exit {exit} is outside the maze bounds.")

    if entry == exit:
        raise ValueError("Entry and exit must be different cells.")
    
    if maze[ex][ey] == 15 or maze[xx][xy] == 15:
        raise ValueError(f"Entry {entry} is inside the 42 block.")
    
    if maze[xx][xy] == 15:
        raise ValueError(f"Exit {exit} is inside the 42 block.")


def main() -> None:
    maze_c = MazeGenerator(
        CONFIG["WIDTH"],
        CONFIG["HEIGHT"],
        CONFIG["ENTRY"],
        CONFIG["EXIT"],
        CONFIG["PERFECT"])
    maze_c.generate()
    maze = maze_c.grid
    validate_entry_exit(CONFIG["ENTRY"], CONFIG["EXIT"], maze)
    render = MazeRenderer(maze)
    regenerate = True

    if not render.check_fits(len(maze), len(maze[0])):
        print("Terminal too small!")
    else:
        while True:
            exit = 0
            os.system("cls" if os.name == "nt" else "clear")
            render.display_maze(maze, regenerate)
            regenerate = False
            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Cycle maze colors")
            print("4. Quit")
            print("5. Cycle 42 color")

            while True:
                choice = input("Choice? (1-5): ").strip()
                if choice == "1":
                    maze_c.generate()
                    maze = maze_c.grid
                    regenerate = True
                    break
                if choice == "3":
                    render.maze_color = render.cycle_color(
                        render.maze_color)
                    break
                elif choice == "4":
                    exit = 1
                    break
                elif choice == "5":
                    render.logo_color = render.cycle_color(
                        render.logo_color)
                    break
            if exit == 1:
                break


main()
