#import sys
#import os
#from maze_gen import MazeGenerator
#from display.render import MazeRenderer
#from parsing import parse_config

#def main():

#    if len(sys.argv) != 2:
#        print("Usage: python3 a_maze_ing.py config.txt")
#        sys.exit(1)
#    filename = sys.argv[1]

#    try:
#        config_data = parse_config(filename)
#    except Exception as e:
#        print(f"Error: {e}")
#        sys.exit(1)
#    maze = MazeGenerator(
#        width=config_data['WIDTH'],
#        height=config_data['HEIGHT'],
#        entry=config_data['ENTRY'],
#        exit=config_data['EXIT'],
#        perfect=config_data['PERFECT'],
#        )

#    try:
#        maze.generate()
#    except Exception as e:
#        print(f"Error generating maze: {e}")
#        sys.exit(1)


#    rendering = MazeRenderer(maze.grid)

#    if not rendering.check_fits(maze.height, maze.width):
#        print("Terminal too small!")
#    else:
#        while True:
#            os.system('cls' if os.name == 'nt' else 'clear')
#            rendering.display_maze(maze.grid)

#            print("\n=== A-Maze-ing ===")
#            print("1. Re-generate a new maze")
#            print("2. Show/Hide path from entry to exit")
#            print("3. Cycle maze colors")
#            print("4. Quit")
#            print("5. Cycle 42 color")

#            choice = input("Choice? (1-5): ").strip()

#            if choice == "3":
#                rendering.cycle_maze_color()
#            elif choice == "5":
#                rendering.cycle_logo_color()
#            elif choice == "4":
#                break

#if __name__ == "__main__":
#    main()
