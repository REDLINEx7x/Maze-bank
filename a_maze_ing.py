from maze_gen import MazeGenerator
from parsing import parse_config
import os
import sys


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

    if maze[ex][ey] == 15:
        raise ValueError(f"Entry {entry} is inside the 42 block.")

    if maze[xx][xy] == 15:
        raise ValueError(f"Exit {exit} is inside the 42 block.")


def main() -> None:
    if len(sys.argv) == 2:
        CONFIG = parse_config(sys.argv[1])
    else:
        raise FileNotFoundError("please enter a config file")

    from display import MazeRenderer
    from maze_solve import solve
    maze_c = MazeGenerator(
        CONFIG["WIDTH"],
        CONFIG["HEIGHT"],
        CONFIG["ENTRY"],
        CONFIG["EXIT"],
        CONFIG["PERFECT"])
    maze_c.generate()
    maze = maze_c.grid
    validate_entry_exit(CONFIG["ENTRY"], CONFIG["EXIT"], maze)
    regenerate = True
    display_solution = False
    render = MazeRenderer(maze)
    if not render.check_fits(len(maze), len(maze[0])):
        print("Terminal too small!")
    else:
        while True:
            exit = 0
            os.system("cls" if os.name == "nt" else "clear")
            sol = solve(maze_c.grid, maze_c.entry, maze_c.exit, maze_c.width, maze_c.height)
            render.display_maze(maze, regenerate, display_solution, sol)
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
                if choice == "2":
                    display_solution = (True if display_solution
                                        is False else False)
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


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print("")
