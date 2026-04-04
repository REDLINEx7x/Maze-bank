import shutil
import time
import os

maze = [[13, 5, 5, 3, 13, 3, 9, 5, 1, 5, 3, 11, 9, 5, 1, 5, 5, 3, 9, 5, 1, 7, 9, 5, 1, 3],
        [9, 5, 7, 12, 3, 10, 10, 11, 10, 13, 2, 10, 12, 3, 12, 5, 3, 14, 10, 11, 12, 5, 4, 7, 10, 10],
        [12, 3, 9, 3, 10, 12, 4, 6, 12, 3, 10, 10, 9, 4, 5, 3, 12, 5, 6, 8, 3, 11, 9, 5, 6, 10],
        [9, 6, 10, 10, 12, 3, 9, 5, 5, 6, 10, 12, 6, 9, 3, 10, 13, 1, 5, 6, 8, 6, 10, 13, 5, 2],
        [10, 9, 6, 12, 3, 10, 10, 13, 5, 3, 12, 5, 5, 6, 10, 12, 5, 6, 9, 7, 10, 9, 6, 9, 3, 14],
        [10, 12, 5, 3, 10, 12, 6, 9, 3, 8, 5, 5, 1, 7, 12, 3, 11, 9, 2, 9, 6, 12, 3, 10, 12, 3],
        [8, 5, 5, 6, 12, 1, 5, 6, 12, 6, 13, 5, 6, 9, 5, 6, 8, 6, 12, 4, 5, 3, 12, 6, 9, 6],
        [10, 13, 3, 9, 5, 2, 9, 5, 5, 3, 9, 5, 3, 12, 3, 13, 6, 9, 5, 3, 9, 6, 9, 7, 12, 3],
        [12, 5, 2, 10, 13, 6, 10, 13, 3, 12, 6, 9, 4, 3, 12, 5, 5, 6, 11, 10, 12, 5, 6, 9, 3, 10],
        [11, 9, 6, 12, 5, 3, 12, 3, 8, 7, 9, 6, 9, 4, 5, 5, 5, 3, 10, 10, 9, 5, 5, 6, 12, 2],
        [8, 6, 9, 3, 9, 4, 7, 10, 10, 15, 8, 3, 14, 15, 15, 15, 11, 12, 2, 10, 8, 3, 9, 1, 7, 10],
        [10, 9, 6, 10, 12, 5, 5, 6, 10, 15, 14, 12, 1, 5, 7, 15, 10, 9, 6, 10, 10, 10, 14, 12, 3, 10],
        [10, 12, 3, 12, 5, 5, 1, 3, 10, 15, 15, 15, 10, 15, 15, 15, 8, 4, 7, 10, 10, 10, 9, 5, 6, 10],
        [10, 13, 0, 5, 5, 7, 10, 12, 4, 5, 3, 15, 10, 15, 13, 5, 4, 3, 9, 6, 10, 10, 12, 5, 5, 6],
        [12, 3, 14, 9, 3, 9, 6, 9, 7, 9, 6, 15, 10, 15, 15, 15, 13, 6, 12, 3, 14, 10, 9, 5, 5, 3],
        [11, 10, 9, 6, 12, 6, 11, 8, 3, 12, 5, 3, 12, 5, 1, 7, 9, 5, 5, 6, 9, 6, 8, 5, 7, 10],
        [10, 12, 6, 9, 5, 5, 2, 10, 12, 5, 3, 10, 13, 3, 12, 3, 12, 3, 9, 7, 8, 5, 6, 9, 3, 10],
        [10, 9, 5, 6, 9, 5, 6, 10, 9, 3, 10, 12, 3, 10, 9, 6, 9, 6, 12, 3, 10, 9, 5, 6, 12, 2],
        [8, 6, 13, 3, 12, 5, 5, 6, 10, 14, 8, 7, 12, 2, 10, 9, 6, 9, 3, 12, 2, 10, 9, 5, 7, 10],
        [10, 9, 3, 8, 5, 3, 13, 5, 4, 3, 12, 5, 5, 6, 10, 10, 9, 6, 12, 3, 10, 10, 12, 1, 5, 6],
        [10, 10, 12, 6, 9, 6, 9, 5, 3, 8, 1, 5, 3, 9, 2, 12, 6, 9, 7, 10, 10, 12, 3, 10, 13, 3],
        [12, 6, 13, 3, 12, 5, 6, 9, 6, 14, 12, 3, 14, 10, 8, 5, 5, 6, 9, 6, 12, 7, 10, 12, 3, 10],
        [9, 5, 5, 0, 5, 5, 7, 10, 13, 1, 1, 6, 9, 6, 14, 9, 5, 3, 12, 5, 5, 5, 6, 9, 6, 10],
        [10, 13, 5, 6, 9, 5, 5, 6, 9, 6, 10, 9, 6, 9, 5, 6, 11, 12, 5, 5, 5, 3, 9, 6, 9, 2],
        [12, 5, 5, 5, 4, 5, 5, 5, 6, 13, 6, 12, 5, 4, 5, 5, 4, 5, 5, 5, 7, 12, 4, 5, 6, 14]]

sol = "SWESNSNS"

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

    def display_maze(self, grid: list[list[int]]) -> None:
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
            time.sleep(self.animation_delay)
            print(mid_line)

        bottom = ""
        for col in range(width):
            bottom += self._get_wall_char(self.corner)
            bottom += self._get_wall_char(self.h_wall)
        bottom += self._get_wall_char(self.corner)
        time.sleep(self.animation_delay)
        print(bottom)

    def check_fits(self, width: int, height: int) -> bool:
        cols, rows = shutil.get_terminal_size()
        needed_cols = width * 4 + 1
        needed_rows = height * 2 + 1
        return needed_cols <= cols and needed_rows <= rows
    
    def display_sol(self, sol: str) -> None:
        for p in sol: #how would I print the path without re rendering the maze, I can't. I must handl the animation dinamically
            if p == "w":
                pass


def main() -> None:
    rendering = MazeRenderer(maze)

    if not rendering.check_fits(len(maze), len(maze[0])):
        print("Terminal too small!")
    else:
        while True:
            exit = 0
            os.system("cls" if os.name == "nt" else "clear")
            rendering.display_maze(maze)

            print("\n=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Cycle maze colors")
            print("4. Quit")
            print("5. Cycle 42 color")

            while True:
                choice = input("Choice? (1-5): ").strip()
                if choice == "1":
                    # implement the logic to call a new maze
                    break
                if choice == "3":
                    rendering.maze_color = rendering.cycle_color(
                        rendering.maze_color)
                    break
                elif choice == "4":
                    exit = 1
                    break
                elif choice == "5":
                    rendering.logo_color = rendering.cycle_color(
                        rendering.logo_color)
                    break
            if exit == 1:
                break


main()
